from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_gemini
from models import User
from routers.auth import authenticate_user
from fastapi.security import OAuth2PasswordBearer
from middleware import get_current_user
router = APIRouter(
    dependencies=[Depends(get_current_user)]  # 👈 this protects all endpoints
)
dom_storage = {}

class ScrapeRequest(BaseModel):
    url: str

class ParseRequest(BaseModel):
    session_id: str

@router.post("/scrape")
def scrape_site(request: ScrapeRequest):
    try:
        html = scrape_website(request.url)
        content = extract_body_content(html)
        cleaned = clean_body_content(content)
        dom_storage[request.url] = cleaned
        return {"session_id": request.url, "cleaned_dom": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse")
def parse_content(request: ParseRequest):
    if request.session_id not in dom_storage:
        raise HTTPException(status_code=404, detail="Session ID not found")
    try:
        dom = dom_storage[request.session_id]
        result = parse_with_gemini(dom)
        return {"parsed_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
