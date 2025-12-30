from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx # ეს ბიბლიოთეკა დაგვეხმარება ტელეგრამთან კავშირში

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- აქ ჩაწერე შენი მონაცემები ---
TELEGRAM_BOT_TOKEN = "8236591512:AAHZ19tGEFisVLf7gW8dQtQGVwkrjqAFM6E"
TELEGRAM_CHAT_ID = "6404415447"
DUMMY_GOOGLE_URL = "https://www.google.com" 
# ------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process-rating")
async def process_rating(rating: int = Form(...)):
    if rating >= 4:
        return RedirectResponse(url=DUMMY_GOOGLE_URL, status_code=303)
    else:
        return RedirectResponse(url=f"/feedback?rating={rating}", status_code=303)

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request, rating: int):
    return templates.TemplateResponse("feedback.html", {"request": request, "rating": rating})

@app.post("/submit-feedback")
async def submit_feedback(rating: int = Form(...), comment: str = Form(...)):
    # ტექსტი, რომელიც მოვა ტელეგრამზე
    message = f"🚨 **ახალი ნეგატიური შეფასება!**\n\n⭐ რეიტინგი: {rating}/5\n💬 კომენტარი: {comment}"
    
    # Telegram API-სთან დაკავშირება
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    async with httpx.AsyncClient() as client:
        await client.post(telegram_url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
    
    return HTMLResponse("<h3>მადლობა! თქვენი შეტყობინება მიღებულია. ადმინისტრაცია უკვე ინფორმირებულია.</h3>")