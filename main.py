from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import create_client

from supabase import create_client

SUPABASE_URL = "sua_url_supabase"
SUPABASE_KEY = "sua_key_supabase"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def humano_ativo(numero):
    atendimento = supabase.table("atendimentos_humanos").select("*").eq("telefone", numero).execute().data
    return bool(atendimento)

@app.post("/webhook-whatsapp")
async def webhook_whatsapp(request: Request):
    data = await request.json()
    numero_remetente = data["phone"]

    # Checa se atendimento humano está ativo
    if humano_ativo(numero_remetente):
        return {"status": "atendimento_humano_ativo"}

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure Supabase (substitua pelas suas credenciais)
SUPABASE_URL = "sua_url_supabase"
SUPABASE_KEY = "sua_key_supabase"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    atendimentos = supabase.table("atendimentos_humanos").select("telefone").execute().data
    numeros = [atendimento["telefone"] for atendimento in atendimentos]
    return templates.TemplateResponse("index.html", {"request": request, "atendimentos": numeros})

@app.post("/toggle")
async def toggle(numero: str = Form(...)):
    atendimento = supabase.table("atendimentos_humanos").select("*").eq("telefone", numero).execute().data
    if atendimento:
        supabase.table("atendimentos_humanos").delete().eq("telefone", numero).execute()
    else:
        supabase.table("atendimentos_humanos").insert({"telefone": numero}).execute()
    return RedirectResponse("/", status_code=303)
