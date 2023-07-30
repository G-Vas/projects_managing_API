from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException

from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas.token import TokenDataSchema
from schemas.users import UserInDBSchema
from core.conf import SECRET_KEY, ALGORITHM
from repositories.base import IRepository
from core.exceptions import CredentialsException, ObjectDoesNotExist
from models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class AuthService:

    repo: IRepository

    def __init__(self, repo: IRepository) -> None:
        self.repo: IRepository = repo

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(self, email: str, password: str) -> User:
        try:
            user = await self.repo.get_by_email(email)
        except ObjectDoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'user with email:{email} does not exist')
        if not self.verify_password(plain_password=password, hashed_password=user.password):
            raise CredentialsException
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise CredentialsException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token_data = TokenDataSchema(email=email)
        except JWTError:
            raise CredentialsException
        user = await self.repo.get_by_email(email=token_data.email)
        if user is None:
            raise CredentialsException
        return user

    async def add_user(self, user: UserInDBSchema) -> User:
        user: dict = user.model_dump()
        user['password'] = self.get_password_hash(user['password'])
        result = await self.repo.add(user)
        return result
