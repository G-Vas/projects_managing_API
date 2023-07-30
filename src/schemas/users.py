from pydantic import BaseModel


class User(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None


class UserInDB(User):
    pass
    password: str
