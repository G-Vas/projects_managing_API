from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None


class UserInDBSchema(UserSchema):
    pass
    password: str
