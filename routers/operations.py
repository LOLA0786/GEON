from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content , structure_of_data
from parse import parse_with_gemini, get_score
from presence import check_brand_visibility_with_gemini
from models import User
from routers.auth import authenticate_user
from fastapi.security import OAuth2PasswordBearer
from middleware import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]  
)
dom_storage = {}

class ScrapeRequest(BaseModel):
    url: str

class ParseRequest(BaseModel):
    session_id: str

class BrandVisibilityRequest(BaseModel):
    brand_name: str

@router.post("/scrape")
def scrape_site(request: ScrapeRequest):
    try:
        html = scrape_website(request.url)  
        content = extract_body_content(html)  
        structure = structure_of_data(content)  
        cleaned = clean_body_content(content)  
        dom_storage[request.url] = {
            "cleaned_content": cleaned,
            "structure": structure,
        }

        return {
            "session_id": request.url,
            "cleaned_dom": cleaned,
            "structure_data": structure
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/parse")
def parse_content(request: ParseRequest):
    if request.session_id not in dom_storage:
        raise HTTPException(status_code=404, detail="Session ID not found")
    try:
        stored_data = dom_storage[request.session_id]
        content = stored_data.get("cleaned_content", "")
        structure = stored_data.get("structure", "")
        if len(structure) == 0 or len(content) == 0:
            return {"parsed_result": result, "msg":"did not not found content or structure"}
        result = parse_with_gemini(content, structure)
        return {"parsed_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-score")
def parse_content(request: ParseRequest):
    if request.session_id not in dom_storage:
        raise HTTPException(status_code=404, detail="Session ID not found")
    try:
        stored_data = dom_storage[request.session_id]
        content = stored_data.get("cleaned_content", "")
        structure = stored_data.get("structure", "")
        if len(structure) == 0 or len(content) == 0:
            return {"parsed_result": result, "msg":"did not not found content or structure"}
        result = get_score(content, structure)
        return {"parsed_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/brand-visibility")
def check_brand_visibility(request: BrandVisibilityRequest):
    try:
        result = check_brand_visibility_with_gemini(request.brand_name)
        return {"visibility_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    