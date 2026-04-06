# 原项目 https://github.com/fastapiadmin/FastapiAdmin/tree/master?tab=readme-ov-file

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


#### 插件化架构特性

- **自动路由发现**：系统会自动扫描 `backend/app/plugin/` 目录下所有 `controller.py` 文件
- **自动路由注册**：所有路由会被自动注册到对应的前缀路径 (module_xxx -> /xxx)
- **模块化管理**：按功能模块组织代码，便于维护和扩展
- **支持多层级嵌套**：支持模块内部多层级嵌套结构

#### 插件目录结构

```sh
backend/app/plugin/
├── module_application/  # 应用模块（自动映射为 /application）
│   └── ai/              # AI子模块
│       ├── controller.py # 控制器文件
│       ├── model.py      # 数据模型文件
│       ├── schema.py     # 数据验证文件
│       ├── service.py    # 业务逻辑文件
│       └── crud.py       # 数据访问文件
├── module_example/      # 示例模块（自动映射为 /example）
│   └── demo/            # 子模块
│       ├── controller.py # 控制器文件
│       ├── model.py      # 数据模型文件
│       ├── schema.py     # 数据验证文件
│       ├── service.py    # 业务逻辑文件
│       └── crud.py       # 数据访问文件
├── module_generator/    # 代码生成模块（自动映射为 /generator）
└── init_app.py          # 插件初始化文件
```


``` bash
backend/app/api
.
├── __init__.py
└── v1
    ├── __init__.py
    ├── module_common
    │   ├── __init__.py
    │   ├── file
    │   │   ├── __init__.py
    │   │   ├── controller.py #文件管理api
    │   │   ├── schema.py
    │   │   └── service.py
    │   └── health
    │       ├── __init__.py
    │       └── controller.py #健康检查api
    ├── module_monitor
    │   ├── __init__.py
    │   ├── cache
    │   │   ├── __init__.py
    │   │   ├── controller.py #缓存监控api
    │   │   ├── schema.py
    │   │   └── service.py
    │   ├── online
    │   │   ├── __init__.py
    │   │   ├── controller.py #在线用户api
    │   │   ├── schema.py
    │   │   └── service.py
    │   ├── resource
    │   │   ├── __init__.py
    │   │   ├── controller.py #资源管理api
    │   │   ├── schema.py
    │   │   └── service.py
    │   └── server
    │       ├── __init__.py
    │       ├── controller.py #服务器监控api
    │       ├── schema.py
    │       └── service.py
    └── module_system
        ├── __init__.py
        ├── auth
        │   ├── __init__.py
        │   ├── controller.py #认证授权api，登录刷新
        │   ├── schema.py
        │   └── service.py
        ├── dept
        │   ├── __init__.py
        │   ├── controller.py #部门管理api
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── dict
        │   ├── __init__.py
        │   ├── controller.py #字典管理
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── log
        │   ├── __init__.py
        │   ├── controller.py #日志管理
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── menu
        │   ├── __init__.py
        │   ├── controller.py #菜单管理
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── notice
        │   ├── __init__.py
        │   ├── controller.py
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── params
        │   ├── __init__.py
        │   ├── controller.py #公告通知
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── position
        │   ├── __init__.py
        │   ├── controller.py #参数管理
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── role
        │   ├── __init__.py
        │   ├── controller.py #角色管理
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── tenant
        │   ├── controlller.py #整个模块注释掉了
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        └── user
            ├── __init__.py
            ├── controller.py  #用户管理
            ├── crud.py
            ├── model.py
            ├── schema.py
            └── service.py
```

```bash
backend/app/plugin
.
├── __init__.py
├── init_app.py
├── module_ai
│   ├── __init__.py
│   └── chat
│       ├── __init__.py
│       ├── controller.py
│       ├── crud.py
│       ├── schema.py
│       ├── service.py
│       ├── utils.py
│       └── ws.py
├── module_application
│   ├── __init__.py
│   └── myapp
│       ├── __init__.py
│       ├── controller.py
│       ├── crud.py
│       ├── model.py
│       ├── schema.py
│       └── service.py
├── module_example
│   ├── __init__.py
│   └── demo
│       ├── __init__.py
│       ├── controller.py
│       ├── crud.py
│       ├── demo01
│       │   ├── __init__.py
│       │   ├── controller.py
│       │   ├── crud.py
│       │   ├── model.py
│       │   ├── schema.py
│       │   └── service.py
│       ├── model.py
│       ├── schema.py
│       └── service.py
├── module_generator
│   ├── __init__.py
│   └── gencode
│       ├── __init__.py
│       ├── controller.py
│       ├── crud.py
│       ├── model.py
│       ├── schema.py
│       ├── service.py
│       ├── templates
│       │   ├── python
│       │   │   ├── __init__.py.j2
│       │   │   ├── controller.py.j2
│       │   │   ├── crud.py.j2
│       │   │   ├── model.py.j2
│       │   │   ├── schema.py.j2
│       │   │   └── service.py.j2
│       │   ├── ts
│       │   │   └── api.ts.j2
│       │   └── vue
│       │       └── index.vue.j2
│       └── tools
│           ├── __init__.py
│           ├── gen_util.py
│           └── jinja2_template_util.py
└── module_task
    ├── __init__.py
    ├── cronjob
    │   ├── __init__.py
    │   ├── job
    │   │   ├── __init__.py
    │   │   ├── controller.py
    │   │   ├── crud.py
    │   │   ├── model.py
    │   │   ├── schema.py
    │   │   └── service.py
    │   └── node
    │       ├── __init__.py
    │       ├── controller.py
    │       ├── crud.py
    │       ├── handlers
    │       │   ├── __init__.py
    │       │   └── demo_handler.py
    │       ├── model.py
    │       ├── schema.py
    │       └── service.py
    └── workflow
        ├── __init__.py
        ├── definition
        │   ├── __init__.py
        │   ├── controller.py
        │   ├── crud.py
        │   ├── model.py
        │   ├── schema.py
        │   └── service.py
        ├── engine
        │   ├── __init__.py
        │   └── prefect_engine.py
        └── node_type
            ├── __init__.py
            ├── controller.py
            ├── crud.py
            ├── model.py
            ├── schema.py
            └── service.py

24 directories, 79 files
```