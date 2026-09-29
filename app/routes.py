import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.schemas import PromptRequest, TestImageRequest
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form("Hero"),
    setting: str = Form("Default Setting"),
    tone: str = Form("Dramatic"),
    art_style: str = Form("Comic Book")
):
    try:
        panels_outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
        enriched_panels = generate_story(panels_outline, character_name, tone)
        image_paths = [
            generate_image(panel["image_prompt"], filename_prefix=f"panel_{panel['panel_number']}")
            for panel in enriched_panels
        ]
        layout = build_comic_layout(enriched_panels, image_paths)
        pdf_path = save_pdf(layout, story_title=story_prompt[:20])
        
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": pdf_path,
                "story_prompt": story_prompt,
                "character_name": character_name
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comic Generation Error: {str(e)}")


@router.post("/generate-comic/json", response_class=JSONResponse)
async def generate_comic_json(payload: PromptRequest):
    try:
        panels_outline = generate_outline(
            payload.story_prompt, 
            payload.character_name, 
            payload.setting, 
            payload.tone, 
            payload.art_style
        )
        enriched_panels = generate_story(panels_outline, payload.character_name, payload.tone)
        image_paths = [
            generate_image(panel["image_prompt"], filename_prefix=f"panel_{panel['panel_number']}") 
            for panel in enriched_panels
        ]
        layout = build_comic_layout(enriched_panels, image_paths)
        pdf_path = save_pdf(layout, story_title=payload.story_prompt[:20])
        
        return JSONResponse(content={"status": "success", "layout": layout, "pdf_path": pdf_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-image", response_class=JSONResponse)
async def test_image_route(payload: TestImageRequest):
    try:
        image_url = generate_image(payload.prompt, filename_prefix="test")
        return JSONResponse(content={"status": "success", "image_url": image_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success_page(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf_path}
    )