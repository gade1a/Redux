from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from tortoise import fields, models
from pydantic import BaseModel
from contextlib import asynccontextmanager

app = FastAPI()

# Exemplo de modelo ORM
class Livro(models.Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    ano = fields.CharField(max_length=4)

    class Meta:
        table = "livros"

# Esquema Pydantic
class LivroIn(BaseModel):
    titulo: str
    autor: str
    ano: str

# Lifespan usando asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    RegisterTortoise(
        app,
        db_url="postgres://postgres:C0rr3t1vO@localhost:5432/postgres",
        modules={"models": ["_main_"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/livros")
async def cadastrar_livro(l: LivroIn):
    novo = await Livro.create(**l.model_dump())
    return {"id": novo.id, "mensagem": "Cadastrado com sucesso"}

@app.get("/livros")
async def listar_livros():
    itens = await Livro.all().values("titulo", "autor", "ano")

    return itens