import os
import re
from PIL import Image, ImageDraw

_sd_pipeline = None

def get_pipeline():
    global _sd_pipeline
    if _sd_pipeline is None:
        try:
            import torch
            from diffusers import StableDiffusionPipeline
            model_id = "runwayml/stable-diffusion-v1-5"
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32
            _sd_pipeline = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
            _sd_pipeline = _sd_pipeline.to(device)
            if device == "cpu": _sd_pipeline.enable_attention_slicing()
        except Exception as e:
            print(f"Warning: Falling back to image generator placeholder ({e})")
            _sd_pipeline = "FALLBACK"
    return _sd_pipeline

def generate_fallback_image(prompt: str, output_path: str):
    img = Image.new('RGB', (512, 512), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 502, 502], outline=(255, 215, 0), width=4)
    draw.rectangle([20, 20, 492, 492], outline=(255, 255, 255), width=2)
    draw.text((30, 180), f"Comic Panel Visual:\n{prompt[:60]}...", fill=(240, 240, 240))
    img.save(output_path)

def generate_image(prompt: str, filename_prefix: str = "panel") -> str:
    os.makedirs("static/panels", exist_ok=True)
    sanitized_prompt = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:20])
    filename = f"{filename_prefix}_{sanitized_prompt}.png"
    output_path = os.path.join("static", "panels", filename)
    pipeline = get_pipeline()
    if pipeline != "FALLBACK":
        try:
            image = pipeline(prompt, num_inference_steps=25).images[0]
            image.save(output_path)
            return f"/static/panels/{filename}"
        except Exception:
            pass
    generate_fallback_image(prompt, output_path)
    return f"/static/panels/{filename}"
