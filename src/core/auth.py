from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from src import dependency
from src.core import configs
from src.db.entity.user_entity import RoleEntity, UserEntity
from src.domain.user.model import user_request
from src.domain.user.model.enums import user_enum

config = configs.config.fastapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def verify_user_state(*, user: UserEntity):
    for state in user.state:
        if str(state.name) == user_enum.UserStateEnum.BLOCKED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="you are blocked",
            )
        elif str(state.name) == user_enum.UserStateEnum.INACTIVATE:
            # TODO
            ...


async def verify_admin(*, role: RoleEntity) -> bool:
    if role.name == user_enum.UserRoleEnum.ADMIN:
        return True
    return False


async def get_current_user(
    *,
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: dependency.UserRepo,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token,
            key=config.auth.secret_key,
            algorithms=config.auth.algorithm,
        )
        username = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user_entity = await user_repo.read_user_by_name(name=username)
        if user_entity is None:
            raise credentials_exception
        await verify_user_state(user=user_entity)

        return user_entity


CurrentUser = Annotated[user_request.UserCurrent, Depends(get_current_user)]
