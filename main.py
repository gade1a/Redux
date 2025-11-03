from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class usuario(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    phone = fields.CharField(max_length=20)
    password_hash = fields.CharField(max_length=128)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

class autor(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

class livro(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    authors = fields.ManyToManyField('models.autor', related_name='books')
    user = fields.ForeignKeyField('models.User', related_name='books')

class cadastrarUsuario(BaseModel):
    nome: str
    email: str
    numero: str
    senha: str

class cadastrarLivro(BaseModel):
    title: str
    authors: list[str]

@app.post("/cadastro")
async def register(user: cadastrarUsuario):
    user_obj = await usuario.create(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=bcrypt.hash(user.password)
    )
    return {"message": "User registered successfully", "user_id": user_obj.id}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await usuario.get_or_none(email=form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.email, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await usuario.get_or_none(email=token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user

@app.post("/books")
async def add_book(book: cadastrarLivro, current_user: usuario = Depends(get_current_user)):
    book_obj = await livro.create(title=book.title, author=book.author, user=current_user)
    return {"message": "Book added successfully", "book_id": book_obj.id}

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),
    modules={"models": ["__main__"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
