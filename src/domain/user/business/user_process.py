from fastapi.security import OAuth2PasswordRequestForm

from src.dependency import ports

from ..model import user_request, user_response
from ..service import login_logic, user_logic, verify_logic


async def create_user(
    *,
    repo: ports.UserRepository,
    data: user_request.UserCreateRequest,
) -> None:
    await verify_logic.verify_user_create(repo=repo, data=data)
    await user_logic.create_user(repo=repo, data=data)


async def login_user(
    *,
    repo: ports.UserRepository,
    form_data: OAuth2PasswordRequestForm,
) -> user_response.Token:
    user = await login_logic.identify_user(repo=repo, form_data=form_data)
    current_user = user_request.UserCurrent.model_validate(obj=user)
    await login_logic.create_login_log(repo=repo, user_id=current_user.id)
    token = await login_logic.create_access_token(username=current_user.name)
    return token


async def update_user(
    *,
    current_user: user_request.UserCurrent,
    repo: ports.UserRepository,
    data: user_request.UserBase,
) -> None:
    await verify_logic.verify_user_update(repo=repo, data=current_user)
    await user_logic.update_user(repo=repo, data=data, current_user=current_user)


async def update_password(
    *,
    current_user: user_request.UserCurrent,
    repo: ports.UserRepository,
    data: user_request.Password,
) -> None:
    await user_logic.update_password(repo=repo, current_user=current_user, data=data)


async def resign_user(
    *,
    current_user: user_request.UserCurrent,
    repo: ports.UserRepository,
) -> None:
    await user_logic.delete_user(repo=repo, current_user=current_user)
