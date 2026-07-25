from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.forum.models import Post
from src.core.database import get_db as _get_db


async def validate_forum_target(target_type: str, target_id: int) -> bool:
    """Validate that a forum target (post or reply) exists.
    Used as a TargetValidator for the interactions app.
    """
    if target_type not in ("post", "reply"):
        return False

    async for db in _get_db():
        if target_type == "post":
            from src.apps.forum.models import Post as PostModel

            stmt = select(PostModel).where(
                PostModel.id == target_id,
                PostModel.deleted_at.is_(None),
            )
        else:
            from src.apps.forum.models import Reply as ReplyModel

            stmt = select(ReplyModel).where(
                ReplyModel.id == target_id,
                ReplyModel.deleted_at.is_(None),
            )

        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None

    return False
