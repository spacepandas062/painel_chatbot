from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from supabase import create_client

# Carrega as credenciais corretamente a partir das variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cliente Supabase único
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para checar atendimento humano ativo
def humano_ativo(numero):
    atendimento = supabase.table("atendimentos_humanos").select("*").eq("telefone", numero).execute().data
    return bool(atendimento)

app = FastAPI()

# Rota webhook do chatbot
@app.post("/webhook-whatsapp")
async def webhook_whatsapp(request: Request):
    data = await request.json()
    numero_remetente = data["phone"]

    # Checa se atendimento humano está ativo
    if humano_ativo(numero_remetente):
        return {"status": "atendimento_humano_ativo"}

    # (adicione sua lógica adicional aqui, se houver)

# Configura pasta estática e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Painel administrativo para controle dos atendimentos
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    atendimentos = supabase.table("atendimentos_humanos").select("telefone").execute().data
    numeros = [atendimento["telefone"] for atendimento in atendimentos]
    return templates.TemplateResponse("index.html", {"request": request, "atendimentos": numeros})

# Ativa ou desativa atendimento humano
@app.post("/toggle")
async def toggle(numero: str = Form(...)):
    atendimento = supabase.table("atendimentos_humanos").select("*").eq("telefone", numero).execute().data
    if atendimento:
        supabase.table("atendimentos_humanos").delete().eq("telefone", numero).execute()
    else:
        supabase.table("atendimentos_humanos").insert({"telefone": numero}).execute()
    return RedirectResponse("/", status_code=303)
