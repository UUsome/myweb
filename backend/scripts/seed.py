import sys
from pathlib import Path

# 把项目源码目录加到 Python 路径
project_root = Path(__file__).parent.parent  # backend/
sys.path.insert(0, str(project_root))


import asyncio

from sqlalchemy import select

from src.apps.users.models import User
from src.apps.users.services import hash_password
from src.apps.experthub.models import TagDefinition, ServiceDefinition
from src.core.database import async_session_factory


async def seed():
    print("🚀 开始初始化种子数据...")
    async with async_session_factory() as db:
        # 1. 创建管理员
        stmt = select(User).where(User.username == "admin")
        result = await db.execute(stmt)
        admin = result.scalar_one_or_none()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                nickname="系统管理员",
                role="admin",
                status="active",
            )
            db.add(admin)
            print("✅ 管理员用户创建成功 (admin / admin123)")
        else:
            print("ℹ️  管理员用户已存在")

        # 2. 创建默认标签
        default_tags = [
            {"name": "AI/人工智能", "slug": "ai", "sort_order": 1},
            {"name": "大数据", "slug": "big-data", "sort_order": 2},
            {"name": "云计算", "slug": "cloud", "sort_order": 3},
            {"name": "前端开发", "slug": "frontend", "sort_order": 4},
            {"name": "后端开发", "slug": "backend", "sort_order": 5},
            {"name": "产品设计", "slug": "product-design", "sort_order": 6},
        ]
        for tag_data in default_tags:
            s = select(TagDefinition).where(TagDefinition.slug == tag_data["slug"])
            r = await db.execute(s)
            if not r.scalar_one_or_none():
                tag = TagDefinition(**tag_data)
                db.add(tag)
                print(f"✅ 标签创建成功: {tag_data['name']}")

        # 3. 创建默认服务形式
        default_services = [
            {"name": "技术咨询", "slug": "consulting", "sort_order": 1},
            {"name": "项目外包", "slug": "outsourcing", "sort_order": 2},
            {"name": "培训/讲师", "slug": "training", "sort_order": 3},
        ]
        for svc_data in default_services:
            s = select(ServiceDefinition).where(ServiceDefinition.slug == svc_data["slug"])
            r = await db.execute(s)
            if not r.scalar_one_or_none():
                svc = ServiceDefinition(**svc_data)
                db.add(svc)
                print(f"✅ 服务形式创建成功: {svc_data['name']}")

        await db.commit()

    print("\n🎉 种子数据初始化完成！")
    print("管理员账号: admin / admin123")
    print("请在首次登录后立即修改密码！")


if __name__ == "__main__":
    asyncio.run(seed())