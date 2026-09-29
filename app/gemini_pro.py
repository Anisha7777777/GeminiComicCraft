import os
import time
from google import genai


def _generate_with_fallback(client, prompt_text: str):
    primary = os.getenv("GEMINI_PRO_MODEL", "gemini-3.8-flash")
    models = list(dict.fromkeys([primary, "gemini-3.5-flash"]))
    last_error = None
    for model in models:
        for attempt in range(2):
            try:
                return client.models.generate_content(model=model, contents=prompt_text)
            except Exception as error:
                last_error = error
                if "503" in str(error) or "UNAVAILABLE" in str(error):
                    time.sleep(2 * (attempt + 1))
                    continue
                raise
    raise RuntimeError(f"Gemini is temporarily unavailable after retrying: {last_error}")


def generate_story(panels_outline: list, character_name: str, tone: str) -> list:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    client = genai.Client(api_key=api_key)
    enriched_panels = []
    for panel in panels_outline:
        prompt_text = f"""
        Write narration and dialogues for Panel {panel.get('panel_number')}:
        - Title: {panel.get('title')}
        - Character Name: {character_name}
        - Scene: {panel.get('scene_description')}
        - Tone: {tone}

        Format output as clean text:
        NARRATION: [Narration text]
        DIALOGUE: {character_name}: "[Dialogue text]"
        """
        response = _generate_with_fallback(client, prompt_text)
        enriched = panel.copy()
        enriched["story_text"] = response.text.strip()
        enriched_panels.append(enriched)
    return enriched_panels
