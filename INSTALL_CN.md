# 🦞 OpenClaw 国内一键安装 (CN Region)

本教程参考官方 `install.sh` 逻辑，并针对中国大陆网络环境进行了如下优化：
1. **Node.js/NPM/Python/Git** 环境自动检测与安装。
2. **NPM 镜像加速**：自动切换至 **阿里镜像 (npmmirror)**，解决 `npm install` 超时问题。
3. **Pip 镜像加速**：自动切换至 **清华大学 (Tsinghua)** 镜像，解决技能依赖包下载慢的问题。
4. **编译加速**：针对 `sharp`、`llama-cpp-node` 等原生模块，配置了自动环境检查以确保编译成功。

---

## 📥 快速安装命令

在终端中运行以下命令（由 NetOps Asset Manager 维护）：

```bash
curl -sSL https://raw.githubusercontent.com/Boos4721/netops-asset-manager-skill/main/scripts/install_openclaw_cn.sh | bash
```

> **注意：** 脚本会自动检测你的系统环境（支持 Ubuntu/Debian/CentOS/Alpine/macOS），并自动配置国内加速镜像。

---

## ⚙️ 脚本核心配置说明 (CN-Optimized)

脚本会自动执行以下核心优化步骤：

### 1. 配置 NPM 镜像 (阿里/淘宝)
解决从官方库下载 `openclaw` 包过慢的问题。
```bash
npm config set registry https://registry.npmmirror.com
```

### 2. 配置 Pip 镜像 (清华大学)
解决技能 (Skills) 在安装 Python 依赖时失败的问题。
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 环境依赖支持
- 自动安装 `build-essential` / `build-base` (make, g++, cmake)。
- 自动安装 `python3` (用于部分 native 模块编译)。
- 确保 Node.js 版本在 **v22+** (官方推荐版本)。

---

## 🛠️ 安装后的操作

安装完成后，你可以直接运行以下命令开始：

1. **初始化配置**：
   ```bash
   openclaw init
   ```
2. **启动后台守护服务**：
   ```bash
   openclaw gateway start
   ```
3. **查看当前 Agent 状态**：
   ```bash
   openclaw status
   ```

---

## 🔧 常见问题排查 (CN Region)

1. **`openclaw` 命令未找到**:
   - 如果你使用的是 macOS 的 `brew` 安装 Node，请确保 `npm bin -g` 的路径已加入你的 `PATH`。
   - 脚本中已尝试自动修复。如果失败，可以尝试重启终端。
2. **GitHub 仓库下载超时**:
   - 脚本中的 `git clone` 已添加了基本的超时重试逻辑。如果依然超时，请考虑配置系统的 `HTTP_PROXY`。
3. **`npm install` 依然报错**:
   - 部分环境需要 `--unsafe-perm`。脚本中已默认带上此参数。

---

## 🐚 开发者支持

由 **NetOps Asset Manager** 维护。如有 Bug 请前往 [GitHub Issues](https://github.com/Boos4721/netops-asset-manager-skill/issues) 反馈。
