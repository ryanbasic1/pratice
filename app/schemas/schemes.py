from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    display_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str   

class NoteCreate(BaseModel):
    title: str
    content: str
  




