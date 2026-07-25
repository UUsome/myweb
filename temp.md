PS E:\web\myweb\backend> .\venv\Scripts\Activate.ps1



pip install -e ".[dev]"

```
把源码移到 src/ 目录下：
backend/
├── src/
│   ├── apps/
│   ├── core/
│   └── admin/
├── alembic/          ← 迁移目录，不在 src 下
├── pyproject.toml
└── ...



```

pip install -e ".[dev]"

pip install asyncpg


(venv) PS E:\web\myweb\backend> $env:DATABASE_URL = "sqlite+aiosqlite:///./myweb.db"
(venv) PS E:\web\myweb\backend>


python -m uvicorn main:app --reload

[info     ] Registered TargetValidator override from forum app
INFO:     Application startup complete.


pip uninstall bcrypt -y
pip install "bcrypt==4.1.3"

====
前端

# 终端 2：启动前端
cd E:\web\myweb\frontend
pnpm dev



cd E:\web\myweb\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
