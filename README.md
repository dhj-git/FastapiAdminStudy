## 🛠️ 二开学习
## 📖 先启动起来

### 后端
```bash
cd backend
uv sync #pyproject.toml

# 启动：请先保证已创建空数据库、Redis 已启动且与 .env.dev 一致
# 首次启动会自动初始化表与基础数据，无需先执行 upgrade

cp backend/env/.env.dev.example backend/env/.env.dev
cp backend/env/.env.prod.example backend/env/.env.prod

cp docker-compose_example.yaml backend/docker-compose.yaml #修改密码那些
#用于部署mysql和redis
docker compose up -d #后台模式启动

# 然后配置 .env.dev  里的mysql和redis信息

uv run main.py run --env=dev #运行

或 uv run main.py run --env=dev 2>&1 | grep -v "DEBUG"

# 生产环境示例
# uv run main.py run --env=prod


```


### 前端
frontend 目录下的 .env.development.example 文件为 .env.development，修改 frontend 目录下的 .env.production.example 文件为 .env.production，然后根据实际情况修改接口地址等。

```bash
cp frontend/.env.development.example frontend/.env.development
cp frontend/.env.production.example frontend/.env.production

cd frontend
pnpm install
pnpm run dev
# 构建生产版本
# pnpm run build

# pnpm --version
# ! Corepack is about to download https://registry.npmjs.org/pnpm/-/pnpm-9.15.3.tgz
# ? Do you want to continue? [Y/n] y

# 9.15.3

# pnpm install
#     ↓
# 读取 package.json（前端的依赖清单）
#     ↓
# 对比 node_modules 里已有的包
#     ↓
# 下载缺少的包
#     ↓
# 安装到 node_modules 文件夹
#     ↓
# 生成/更新 pnpm-lock.yaml（锁定版本）

# 可能会出现Socket timeout错误，解决方法如下
# 设置淘宝镜像
pnpm config set registry https://registry.npmmirror.com
# 验证是否设置成功
pnpm config get registry
# 输出：https://registry.npmmirror.com
# 重新安装
pnpm install
```
运行之后开启页面

**初始登录账号和密码**：👤 登录账号：admin 密码：123456
