from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

atendimento_humano_ativo = set()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "atendimentos": atendimento_humano_ativo})

@app.post("/toggle")
async def toggle(numero: str = Form(...)):
    if numero in atendimento_humano_ativo:
        atendimento_humano_ativo.remove(numero)
    else:
        atendimento_humano_ativo.add(numero)
    return RedirectResponse("/", status_code=303)
