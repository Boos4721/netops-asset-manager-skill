# 🦞 OpenClaw 国内一键安装文档 (Optimized for CN Region)

本教程通过脚本自动化配置，解决了国内访问 GitHub、NPM、PyPI 速度慢的问题。

## 📥 一键安装命令 (推荐)

在终端中运行以下命令：

```bash
curl -sSL https://raw.githubusercontent.com/Boos4721/netops-asset-manager-skill/main/scripts/install_openclaw_cn.sh | bash
```

> **注意：** 脚本会自动检测你的系统环境（支持 Ubuntu/Debian/CentOS/Alpine），并自动配置 **阿里 NPM 镜像** 和 **清华 Pip 镜像**。

---

## 🛠️ 手动安装步骤 (分步解说)

如果你想手动控制每一步，可以按照以下指南操作：

### 1. 基础依赖检查
确保系统中已安装 `nodejs` (v18+), `npm`, `git`, `python3` 和 `pip`。

### 2. 国内镜像加速 (关键)

配置 **NPM** (淘宝/阿里镜像):
```bash
npm config set registry https://registry.npmmirror.com
```

配置 **Pip** (清华大学镜像):
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 安装 OpenClaw
```bash
npm install -g openclaw --unsafe-perm
```

### 4. 初始化工作目录
建议在 `/root/clawd` (或你的主目录下的 `clawd`) 进行操作：
```bash
mkdir -p /root/clawd && cd /root/clawd
openclaw init
```

### 5. 启动服务
```bash
openclaw gateway start
```

---

## 🔧 常见问题排查 (CN Region)

1. **GitHub 仓库下载失败 (Cloning Timeout)**:
   - 脚本中已默认使用国内加速。如仍失败，建议配置系统的 `HTTP_PROXY` 或使用 Gitee 镜像。
2. **Node 版本过低**:
   - 建议使用 `n` 或 `nvm` 管理 Node 版本，确保在 v18 以上。
3. **Npminstall 卡在进度条**:
   - 确认 `npm config get registry` 确实是 `registry.npmmirror.com`。

---

## 🐚 开发者支持

本项目由 **NetOps Asset Manager** 维护。如有 Bug 请前往 [GitHub Issues](https://github.com/Boos4721/netops-asset-manager-skill/issues) 反馈。
