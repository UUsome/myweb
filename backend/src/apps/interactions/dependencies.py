from __future__ import annotations

from typing import Annotated, Protocol, Any

from fastapi import Depends, Path

from src.apps.interactions.models import TargetValidator as TargetValidatorProtocol
from src.apps.users.dependencies import get_current_user
from src.apps.users.models import User
from src.core.logger import get_logger

logger = get_logger(__name__)

# This is the dependency override target
# Forum app registers its implementation in main.py lifespan
TargetValidator = TargetValidatorProtocol

# Supported target types
VALID_TARGET_TYPES = {"post", "reply", "expert", "job"}


async def validate_target_type(
    target_type: str = Path(..., description="目标类型"),
) -> str:
    """Validate that the target type is supported."""
    if target_type not in VALID_TARGET_TYPES:
        raise ValueError(f"不支持的目标类型: {target_type}")
    return target_type


async def verify_target_exists(
    target_type: str = Depends(validate_target_type),
    target_id: int = Path(..., description="目标 ID"),
    validator: Any = None,
) -> tuple[str, int]:
    """Verify that the target exists using the registered validator."""
    if validator is not None:
        exists = await validator(target_type, target_id)
        if not exists:
            from src.core.exceptions import NotFound

            raise NotFound(message=f"{target_type} 不存在")
    return target_type, target_id

