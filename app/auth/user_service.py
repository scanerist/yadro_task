from app.auth.dao import UsersDAO
from app.auth.utils import get_password_hash, verify_password
from app.auth.token_service import TokenService
from app.auth.schemas import UserRegister, UserRead
from app.exceptions import UserAlreadyExistsException, IncorrectPasswordException

class AuthService:
    @staticmethod
    async def register(session, user_data: UserRegister):
        dao = UsersDAO(session)
        existing = await dao.find_one_or_none(filters={"username": user_data.username})
        if existing:
            raise UserAlreadyExistsException
        hashed_password = get_password_hash(user_data.password)
        user = await dao.add({"username": user_data.username, "password_hash": hashed_password})
        return UserRead.model_validate(user).model_dump()

    @staticmethod
    async def authenticate(session, username: str, password: str):
        dao = UsersDAO(session)
        user = await dao.find_one_or_none(filters={"username": username})
        if not user or not verify_password(password, user.password_hash):
            raise IncorrectPasswordException
        return user

    @staticmethod
    def create_token(user_id: int):
        return TokenService.create_access_token(data={"sub": str(user_id)})
