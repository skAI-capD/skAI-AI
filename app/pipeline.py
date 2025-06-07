from app.prompt_utils import correct_diary, summarize_main_scene, get_character_prompt, build_diary_prompt
from app.image_utils import generate_all_images

# 전체 실행 파이프라인
def run_diary_image_pipeline(
    diary_text: str,
    gender: str,
    style: str,
    color: str,
    use_custom: bool,
    hairstyle: str = "",
    outfit: str = ""
) -> dict:
    corrected = correct_diary(diary_text)
    scene = summarize_main_scene(corrected)
    character_prompt = get_character_prompt(gender, use_custom, hairstyle, outfit)
    full_prompt = build_diary_prompt(scene, style, color, character_prompt)
    image_urls = generate_all_images(full_prompt)

    return {
        "correctedText": corrected,
        "mainScene": scene,
        "characterPrompt": character_prompt,
        "prompt": full_prompt,
        "imageUrls": image_urls
    }