from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    story_prompt: str = Field(..., example="A brave fox exploring an enchanted forest.")
    character_name: str = Field(default="Hero", example="Felix")
    setting: str = Field(default="Enchanted Forest", example="Forest")
    tone: str = Field(default="Dramatic", example="Dramatic")
    art_style: str = Field(default="Anime", example="Anime")

class TestImageRequest(BaseModel):
    prompt: str = Field(..., example="A comic panel of a brave fox in an enchanted glowing forest, anime style")
