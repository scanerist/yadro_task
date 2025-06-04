from typing import Optional

from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "access_token": "slkfjaksdfjlasdfjlasdfjlasdfj",
                "token_type": "bearer"
            }
        }
    )




class UserRegister(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "username": "alias_user",
                "password": "securepasswordforalias123"
            }
        }
    )

class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
