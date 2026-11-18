from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=1, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=1, le=120)
    password: str = Field(min_length=8)

class MessageResponse(BaseModel):
    message: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
