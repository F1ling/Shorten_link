from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, AnyUrl
import secrets
import datetime
from typing import Dict
import re

app = FastAPI(title="Сервис сокращения ссылок")


templates = Jinja2Templates(directory="shortener-service/app/templates")

# Хранилище ссылок в памяти
url_storage: Dict[str, dict] = {}

class URLRequest(BaseModel):
    url: AnyUrl

def generate_short_code():
    #Генерация короткого кода
    return secrets.token_urlsafe(6)[:8]

def is_valid_url(url: str) -> bool:
    #Проверка валидности URL
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// или https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # домен
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # или ip
        r'(?::\d+)?'  # порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.post("/shorten")
async def shorten_url(url_request: URLRequest):
    #Создание короткой ссылки
    if not is_valid_url(str(url_request.url)):
        raise HTTPException(status_code=400, detail="Некорректный URL")
    
    short_code = generate_short_code()
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    
    url_storage[short_code] = {
        "original_url": str(url_request.url),
        "created_at": datetime.datetime.now(),
        "expires_at": expiration_time
    }
    
    return {"short_url": f"/{short_code}"}

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    #Перенаправление по короткой ссылке
    if short_code not in url_storage:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    
    url_data = url_storage[short_code]
    
    if datetime.datetime.now() > url_data["expires_at"]:
        del url_storage[short_code]
        raise HTTPException(status_code=410, detail="Ссылка истекла")
    
    return RedirectResponse(url_data["original_url"])

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    #Главная страница с формой
    return templates.TemplateResponse("base.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload= True)