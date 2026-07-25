Created 12 todos

Let me start building this project. First, I'll create the directory structure.

Created [](file:///e%3A/web/myweb/backend)

Created [](file:///e%3A/web/myweb/backend/apps/core)

Created [](file:///e%3A/web/myweb/backend/apps/users/tests)

Created [](file:///e%3A/web/myweb/backend/apps/forum/tests)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/tests)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/tests)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/tests)

Created [](file:///e%3A/web/myweb/backend/core)

Created [](file:///e%3A/web/myweb/backend/admin)

Created [](file:///e%3A/web/myweb/backend/alembic/versions)

Now let me create all the project files. I'll start with the configuration and core components.

Created [](file:///e%3A/web/myweb/backend/.env.example)

Created [](file:///e%3A/web/myweb/backend/.env)

Created [](file:///e%3A/web/myweb/backend/pyproject.toml)

Created [](file:///e%3A/web/myweb/backend/pytest.ini)

Now let me create the core project configuration files.

Created [](file:///e%3A/web/myweb/backend/core/__init__.py)

Created [](file:///e%3A/web/myweb/backend/core/config.py)

Created [](file:///e%3A/web/myweb/backend/core/database.py)

Created [](file:///e%3A/web/myweb/backend/core/logger.py)

Now let me create the core app files.

Created [](file:///e%3A/web/myweb/backend/apps/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/base_model.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/base_repository.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/pagination.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/base_schema.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/response.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/middleware.py)

Created [](file:///e%3A/web/myweb/backend/apps/core/dependencies.py)

Now let me build the Users app - models, schemas, services, JWT auth, and router.

Created [](file:///e%3A/web/myweb/backend/apps/users/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/models.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/schemas.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/services.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/dependencies.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/router.py)

Created [](file:///e%3A/web/myweb/backend/apps/users/admin.py)

Now let me build the Forum app.

Created [](file:///e%3A/web/myweb/backend/apps/forum/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/models.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/schemas.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/services.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/dependencies.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/router.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/forum/admin.py)

Starting: *Setup database & Alembic* (6/12)

Now let me create the Interactions app.

Created [](file:///e%3A/web/myweb/backend/apps/interactions/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/models.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/schemas.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/services.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/dependencies.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/router.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/interactions/admin.py)

Now let me create the ExpertHub app.

Created [](file:///e%3A/web/myweb/backend/apps/experthub/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/models.py)

Let me fix the ExpertHub models - the association tables need proper SQLAlchemy column usage.

Created [](file:///e%3A/web/myweb/backend/apps/experthub/models.py)




```

```
Now let me create the remaining ExpertHub files and the JobHub app.

Created [](file:///e%3A/web/myweb/backend/apps/experthub/schemas.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/services.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/dependencies.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/router.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/experthub/admin.py)

Now let me create the JobHub app.

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/__init__.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/models.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/schemas.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/services.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/dependencies.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/exceptions.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/router.py)

Created [](file:///e%3A/web/myweb/backend/apps/jobhub/admin.py)

Now let me create the Admin site and main entry point.

Created [](file:///e%3A/web/myweb/backend/admin/__init__.py)

Created [](file:///e%3A/web/myweb/backend/admin/site.py)

Now let me create the main entry point - `main.py`.

Created [](file:///e%3A/web/myweb/backend/main.py)

Let me fix an issue in the jobhub services and create the Alembic config.



Read [](file:///e%3A/web/myweb/backend/apps/jobhub/services.py#104-104), lines 104 to 145




```

```
Now let me create the Alembic configuration.

Created [](file:///e%3A/web/myweb/backend/alembic.ini)

Created [](file:///e%3A/web/myweb/backend/alembic/env.py)

Created [](file:///e%3A/web/myweb/backend/alembic/script.py.mako)

Created [](file:///e%3A/web/myweb/backend/alembic/README)

Completed: *Setup database & Alembic* (6/12)

Let me verify the complete project structure.

Ran terminal command: Get-ChildItem -Recurse -Name e:\web\myweb\backend | Sort-Object

The complete FastAPI 可插拔 App 架构项目已全部生成。以下是项目总览：

---

## 项目结构

```
backend/
├── main.py                          # 入口（lifespan + 可插拔加载）
├── core/                            # 项目级配置
│   ├── config.py                    # Pydantic Settings
│   ├── database.py                  # asyncpg 连接池
│   └── logger.py                    # structlog 配置
├── apps/
│   ├── core/                        # 共享核心库（8个模块）
│   │   ├── base_model.py            # 时间戳 + 软删除 Mixin
│   │   ├── base_repository.py       # 通用 CRUD
│   │   ├── pagination.py            # 游标分页 + 偏移分页
│   │   ├── base_schema.py           # Pydantic 基类
│   │   ├── response.py              # 统一响应格式 {code, message, data, timestamp}
│   │   ├── exceptions.py            # 全局异常处理器（含 10 种异常类）
│   │   ├── middleware.py            # 请求日志中间件（request_id + 环境标识）
│   │   └── dependencies.py          # 通用依赖（分页/排序）
│   ├── users/                       # 用户管理 + JWT 认证（9个API）
│   ├── forum/                       # 论坛（板块/帖子/回复，12个API）
│   ├── interactions/                # 点赞/评论（多态，7个API）
│   ├── experthub/                   # 专家卡片（标签/平台/案例，18个API）
│   └── jobhub/                      # 人才集市/职位（8个API）
├── admin/                           # 自建轻量级 Admin 后台
│   └── site.py                      # AdminSite + ModelAdmin 基类
├── alembic/                         # 数据库迁移
│   ├── env.py                       # 异步 Alembic 配置
│   └── versions/
├── pyproject.toml
├── pytest.ini
├── .env / .env.example
└── alembic.ini
```

## 关键特性实现

| 特性 | 实现位置 |
|------|----------|
| **可插拔加载** | `main.py` - `ENABLED_APPS` + `importlib.import_module` |
| **统一响应格式** | `apps/core/response.py` - `APIResponse {code, message, data, timestamp}` |
| **全局异常处理** | `apps/core/exceptions.py` - HTTPException + 通用 Exception 兜底 |
| **请求日志中间件** | `apps/core/middleware.py` - request_id + X-Request-ID/X-Environment/X-API-Version |
| **JWT 认证** | `apps/users/services.py` - Access（15分）+ Refresh（7天，Redis） |
| **TargetValidator Protocol** | `apps/interactions/models.py` → `main.py` lifespan 中注册 |
| **板块树缓存** | `apps/forum/services.py` - 进程内缓存 TTL 5分钟 |
| **游标分页** | `apps/core/pagination.py` - 无限滚动场景 |
| **偏移分页** | `apps/core/pagination.py` - Admin 后台场景 |
| **软删除** | `apps/core/base_repository.py` - `soft_delete`/`restore` |
| **Admin 后台** | `admin/site.py` - 自建轻量级 + 独立路由 `/admin/api/` |
| **501 保留接口** | `apps/users/router.py` - 注册/验证接口返回 501 |

## API 概览

- **Users** (9): 登录/刷新/登出/个人信息 + 3个501保留接口
- **Forum** (12): 板块CRUD + 帖子CRUD + 回复列表/发表
- **Interactions** (7): 点赞切换/状态/计数 + 评论列表/发表/删除
- **ExpertHub** (18): 专家列表/详情/Hover + 平台/案例CRUD + 标签/服务
- **JobHub** (8): 职位列表/详情/筛选/标签 + Admin CRUD + 置顶切换
- **Admin API**: 自动为每个注册模型生成 CRUD 接口

## 依赖关系

```
core → users → { forum, interactions, experthub } → jobhub
```

## 启动方式

```bash
cd backend
pip install -e ".[dev]"
alembic upgrade head
uvicorn main:app --reload
```

访问 `http://localhost:8000/docs` 查看自动生成的 OpenAPI 文档。

Made changes.