import os
import json
import time
from google import genai
from google.genai import types


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)


def _generate_with_fallback(client, prompt_text: str):
    primary = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash")
    models = list(dict.fromkeys([primary, "gemini-3.5-flash"]))
    last_error = None
    for model in models:
        for attempt in range(2):
            try:
                return client.models.generate_content(
                    model=model,
                    contents=prompt_text,
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
            except Exception as error:
                last_error = error
                if "503" in str(error) or "UNAVAILABLE" in str(error):
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
    raise RuntimeError(f"Gemini is temporarily unavailable after retrying: {last_error}")


def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> list:
    client = get_gemini_client()
    prompt_text = f"""
    Create a 5-panel comic strip outline based on:
    - Story Idea: {story_prompt}
    - Main Character: {character_name}
    - Setting: {setting}
    - Story Tone: {tone}
    - Art Style: {art_style}

    Return a strictly formatted JSON list containing 5 panel objects.
    Each object MUST have: "panel_number", "title", "scene_description", "image_prompt".
    """
    response = _generate_with_fallback(client, prompt_text)
    clean_text = response.text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    return json.loads(clean_text.strip())
