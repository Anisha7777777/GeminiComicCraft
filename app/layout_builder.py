def build_comic_layout(enriched_panels: list, image_paths: list) -> list:
    layout = []
    for idx, panel in enumerate(enriched_panels):
        img_path = image_paths[idx] if idx < len(image_paths) else "/static/panels/placeholder.png"
        layout.append({
            "panel_number": panel.get("panel_number", idx + 1),
            "title": panel.get("title", f"Panel {idx + 1}"),
            "scene_description": panel.get("scene_description", ""),
            "image_path": img_path,
            "story_text": panel.get("story_text", ""),
            "image_prompt": panel.get("image_prompt", "")
        })
    return layout
