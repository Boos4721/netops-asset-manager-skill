#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import subprocess
import psycopg2
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import httpx
import asyncio
from health_prober import ping_check

# Resolve paths
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SKILL_DIR, 'assets')
INVENTORY_FILE = os.path.join(ASSETS_DIR, 'inventory.json')
MODELS_FILE = os.path.join(ASSETS_DIR, 'models.json')
LOGS_DIR = os.path.join(ASSETS_DIR, 'logs')
UPLOAD_DIR = os.path.join(ASSETS_DIR, 'uploads')
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_openclaw_models():
    """Read models from OpenClaw config"""
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        models_config = config.get('models', {})
        providers = models_config.get('providers', {})
        
        all_models = []
        for provider_name, provider_config in providers.items():
            base_url = provider_config.get('baseUrl', '')
            api_key = provider_config.get('apiKey', '')
            for model in provider_config.get('models', []):
                all_models.append({
                    'id': model.get('id'),
                    'name': model.get('name'),
                    'provider': provider_name,
                    'base_url': base_url,  # frontend uses base_url
                    'api_key': api_key,   # frontend may need this
                    'reasoning': model.get('reasoning', False),
                    'input': model.get('input', []),
                    'contextWindow': model.get('contextWindow'),
                    'maxTokens': model.get('maxTokens'),
                    'cost': model.get('cost', {}),
                    'enabled': True,
                    'source': 'openclaw'
                })
        return all_models
    except Exception as e:
        print(f"Error reading OpenClaw models: {e}")
        return []

def save_openclaw_models(providers_data):
    """Save models back to OpenClaw config"""
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'models' not in config:
            config['models'] = {}
        config['models']['providers'] = providers_data
        
        with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving OpenClaw models: {e}")
        return False

def get_providers_from_config():
    """Get providers dict from OpenClaw config"""
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('models', {}).get('providers', {})
    except Exception:
        return {}

# DB config
DB_CONFIG = {
    "dbname": "netops",
    "user": "postgres",
    "password": "boos",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def read_json(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

app = FastAPI(title="NetOps API", description="Advanced API for NetOps Dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for Validation
class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

class LoginRequest(BaseModel):
    username: str
    password: str



class UserRequest(BaseModel):
    username: str
    password: str
    role: str = "operator"

class DeployRequest(BaseModel):
    task_name: str
    binary_path: str
    args: str = ""
    target_ips: List[str] = []

class SystemDeployRequest(BaseModel):
    type: str  # 'docker', 'vllm', 'llama-cpp'

@app.post("/api/deploy/system")
async def deploy_system_feature(req: SystemDeployRequest):
    """Execute system-level deployment tasks in background via PM2/Subprocess"""
    commands = {
        "docker": "curl -fsSL https://get.docker.com | sh",
        "vllm": "pip install vllm",
        "llama-cpp": "git clone https://github.com/ggerganov/llama.cpp.git /tmp/llama.cpp && cd /tmp/llama.cpp && make"
    }
    
    cmd = commands.get(req.type)
    if not cmd:
        raise HTTPException(status_code=400, detail="Invalid deployment type")
        
    try:
        # Use PM2 to run these as one-shot tasks so we can monitor them in the UI
        task_name = f"deploy-{req.type}-{os.urandom(2).hex()}"
        pm2_cmd = ["pm2", "start", cmd, "--name", task_name, "--no-autorestart"]
        subprocess.Popen(pm2_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "success", "message": f"任务 {task_name} 已在后台启动，请在 PM2 列表中查看进度。"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Proxy chat requests to OpenClaw CLI agent"""
    try:
        # Build the conversation context
        system_prompt = """你是一个专业的 NetOps 网络运维助理。你能够帮助用户管理资产、监控任务、分析日志。

**核心能力：资产录入**
如果用户要求录入或添加资产（例如："录入一台 10.1.1.1 的 H3C 交换机"），请你在回复的最后添加一行特殊的标记：
`ACTION: ADD_ASSET | IP: <IP地址> | VENDOR: <品牌> | NAME: <设备名>`
例如：`ACTION: ADD_ASSET | IP: 10.1.1.1 | VENDOR: H3C | NAME: H3C-Switch-01`

请保持专业、简洁、高效的语气。"""

        # Build full prompt with history
        history_text = ""
        for msg in req.history[-10:]:
            role = "User" if msg.get("from") == "user" else "Assistant"
            history_text += f"{role}: {msg.get('text', '')}\n"
        
        full_prompt = f"{system_prompt}\n\n---\n历史对话:\n{history_text}\n---\nUser: {req.message}\nAssistant:"
        
        # Call OpenClaw agent via subprocess (use a fixed session for continuity)
        proc = subprocess.run(
            ["openclaw", "agent", "--session-id", "netops-chat", "--message", full_prompt, "--timeout", "60", "--json"],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        if proc.returncode == 0:
            import json
            try:
                result = json.loads(proc.stdout)
                # Extract reply from JSON output
                reply_text = result.get("reply", "")
                if reply_text:
                    # It might be a nested JSON string
                    try:
                        inner = json.loads(reply_text)
                        reply = inner.get("text", inner.get("content", reply_text))
                    except:
                        reply = reply_text
                else:
                    # Fallback: try to parse from result.result.payloads
                    payloads = result.get("result", {}).get("payloads", [])
                    if payloads:
                        reply = payloads[0].get("text", "")
                    else:
                        reply = str(result)
                return {"status": "success", "reply": reply}
            except Exception as e:
                return {"status": "success", "reply": proc.stdout.strip()[:500]}
        else:
            return {"status": "error", "message": f"OpenClaw error: {proc.stderr}"}
                
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/inventory")
async def get_inventory():
    inventory = read_json(INVENTORY_FILE)
    
    # Run health checks in parallel to avoid blocking the event loop
    async def check_device(device):
        ip = device.get('ip')
        if ip:
            loop = asyncio.get_event_loop()
            # Offload synchronous ping_check to a thread pool
            is_online = await loop.run_in_executor(None, ping_check, ip)
            device['status'] = 'online' if is_online else 'offline'
        return device

    tasks = [check_device(d) for d in inventory]
    return await asyncio.gather(*tasks)

@app.post("/api/inventory/add")
async def add_inventory(payload: Request):
    data = await payload.json()
    inventory = read_json(INVENTORY_FILE)
    inventory.append(data)
    write_json(INVENTORY_FILE, inventory)
    return {"status": "success"}

@app.put("/api/inventory/{ip}")
async def update_inventory(ip: str, payload: Request):
    data = await payload.json()
    inventory = read_json(INVENTORY_FILE)
    for i, dev in enumerate(inventory):
        if dev.get('ip') == ip:
            inventory[i].update(data)
            write_json(INVENTORY_FILE, inventory)
            return {"status": "success"}
    raise HTTPException(status_code=404, detail="Device not found")

@app.delete("/api/inventory/{ip}")
async def delete_inventory(ip: str):
    inventory = read_json(INVENTORY_FILE)
    new_inventory = [d for d in inventory if d.get('ip') != ip]
    if len(new_inventory) == len(inventory):
        raise HTTPException(status_code=404, detail="Device not found")
    write_json(INVENTORY_FILE, new_inventory)
    return {"status": "success"}

@app.get("/api/stats")
async def get_stats():
    inventory = read_json(INVENTORY_FILE)
    return {
        "total": len(inventory),
        "online": sum(1 for d in inventory if d.get('status') == 'online'),
        "alerts": 0,
        "gpu_count": sum(1 for d in inventory if d.get('gpu'))
    }

@app.get("/api/logs")
async def get_logs():
    return [{"id": 1, "time": "System", "level": "info", "message": "API Started", "detail": ""}]

@app.get("/api/users")
async def get_users():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, role FROM users")
                return [{"id": r[0], "username": r[1], "role": r[2]} for r in cur.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/login")
async def login(req: LoginRequest):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (req.username, req.password))
                user = cur.fetchone()
                if user:
                    return {"status": "success", "token": "mock_token", "role": user[1], "username": req.username}
                return {"status": "error", "message": "Invalid credentials"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/users")
async def create_user(req: UserRequest):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (req.username, req.password, req.role))
                conn.commit()
                return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
                conn.commit()
                return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/models")
async def get_models():
    # Read from OpenClaw config (synchronized)
    return get_openclaw_models()

@app.get("/api/providers")
async def get_providers():
    """Get list of available providers"""
    providers = get_providers_from_config()
    return list(providers.keys())

@app.post("/api/models/add")
async def add_model(payload: Request):
    """Add a new model to OpenClaw config"""
    try:
        data = await payload.json()
        providers = get_providers_from_config()
        
        # Get provider info from request
        provider_name = data.get('provider', 'custom')
        
        # Fix: ensure contextWindow and maxTokens are not null
        context_window = data.get('contextWindow')
        max_tokens = data.get('maxTokens')
        
        model_data = {
            'id': data.get('id') or data.get('name', 'custom-model').lower().replace(' ', '-'),
            'name': data.get('name'),
            'reasoning': data.get('reasoning', False),
            'input': data.get('input', ['text']),
            'contextWindow': int(context_window) if context_window is not None else 4096,
            'maxTokens': int(max_tokens) if max_tokens is not None else 4096,
            'cost': data.get('cost', {})
        }
        
        # Handle field name differences (frontend uses base_url/api_key)
        base_url = data.get('base_url') or data.get('baseUrl', 'https://api.custom.com/v1')
        api_key = data.get('api_key') or data.get('apiKey', '')
        
        # Add to provider (create provider if not exists)
        if provider_name not in providers:
            providers[provider_name] = {
                'baseUrl': base_url,
                'apiKey': api_key,
                'api': 'openai-completions',
                'models': []
            }
        
        providers[provider_name]['models'] = providers[provider_name].get('models', [])
        providers[provider_name]['models'].append(model_data)
        
        if save_openclaw_models(providers):
            return {"status": "success", "message": f"模型 {data.get('name')} 添加成功"}
        return {"status": "error", "message": "保存配置失败"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.put("/api/models/{model_id}")
async def update_model(model_id: str, payload: Request):
    """Update a model in OpenClaw config"""
    try:
        data = await payload.json()
        providers = get_providers_from_config()
        
        # Fix: ensure contextWindow and maxTokens are not null
        context_window = data.get('contextWindow')
        max_tokens = data.get('maxTokens')
        
        # Find and update the model
        for provider_name, provider_config in providers.items():
            models = provider_config.get('models', [])
            for i, model in enumerate(models):
                if model.get('id') == model_id:
                    # Update model fields
                    models[i].update({
                        'name': data.get('name', model.get('name')),
                        'reasoning': data.get('reasoning', model.get('reasoning')),
                        'input': data.get('input', model.get('input')),
                        'contextWindow': int(context_window) if context_window is not None else model.get('contextWindow', 4096),
                        'maxTokens': int(max_tokens) if max_tokens is not None else model.get('maxTokens', 4096),
                        'cost': data.get('cost', model.get('cost', {}))
                    })
                    provider_config['models'] = models
                    
                    if save_openclaw_models(providers):
                        return {"status": "success", "message": "模型更新成功"}
                    return {"status": "error", "message": "保存配置失败"}
        
        return {"status": "error", "message": "模型未找到"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/models/set-default")
async def set_default_model(payload: Request):
    """Set the primary model for OpenClaw agents"""
    try:
        data = await payload.json()
        model_id = data.get('model_id')
        provider_name = data.get('provider')
        
        if not model_id or not provider_name:
            return {"status": "error", "message": "Missing model_id or provider"}
            
        full_model_id = f"{provider_name}/{model_id}"
        
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        if 'agents' not in config: config['agents'] = {}
        if 'defaults' not in config['agents']: config['agents']['defaults'] = {}
        if 'model' not in config['agents']['defaults']: config['agents']['defaults']['model'] = {}
        
        config['agents']['defaults']['model']['primary'] = full_model_id
        
        with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        return {"status": "success", "message": f"默认模型已设置为 {full_model_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/api/models/{model_id}")
async def delete_model(model_id: str):
    """Delete a model from OpenClaw config"""
    try:
        providers = get_providers_from_config()
        
        for provider_name, provider_config in providers.items():
            models = provider_config.get('models', [])
            new_models = [m for m in models if m.get('id') != model_id]
            
            if len(new_models) != len(models):
                provider_config['models'] = new_models
                
                if save_openclaw_models(providers):
                    return {"status": "success", "message": "模型删除成功"}
                return {"status": "error", "message": "保存配置失败"}
        
        return {"status": "error", "message": "模型未找到"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/pm2/status")
async def get_pm2_status():
    try:
        result = subprocess.check_output(["pm2", "jlist"]).decode()
        pm2_list = json.loads(result)
        tasks = [{
            "name": p.get("name"),
            "status": p.get("pm2_env", {}).get("status"),
            "restarts": p.get("pm2_env", {}).get("restart_time"),
            "memory": p.get("monit", {}).get("memory"),
            "cpu": p.get("monit", {}).get("cpu")
        } for p in pm2_list]
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pm2/deploy")
async def deploy_pm2_task(req: DeployRequest):
    """Deploy task to remote machines via SSH + PM2"""
    results = []
    ssh_user = "root"  # default SSH user
    
    for ip in req.target_ips:
        try:
            # Build the PM2 command (quote the binary path for safety)
            pm2_cmd = f"pm2 start \"{req.binary_path}\""
            if req.args:
                pm2_cmd += f" -- {req.args}"
            pm2_cmd += f" --name {req.task_name}"
            
            # SSH and run PM2 command on remote machine
            ssh_cmd = [
                "ssh", "-o", "StrictHostKeyChecking=no",
                f"{ssh_user}@{ip}",
                pm2_cmd
            ]
            
            subprocess.check_call(ssh_cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            results.append({"ip": ip, "status": "deployed", "cmd": pm2_cmd})
        except subprocess.CalledProcessError as e:
            results.append({"ip": ip, "status": "failed", "error": str(e)})
        except Exception as e:
            results.append({"ip": ip, "status": "failed", "error": str(e)})
            
    return {"status": "success", "results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
