from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from .evaluator import evaluate

load_dotenv()

app = FastAPI(title="MCP Eval Server")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/evaluate")
async def evaluate_endpoint(request: Request):
    body = await request.json()
    message = body.get("message", "")
    result = evaluate(message)
    return JSONResponse({"response": result})