from openai import OpenAI
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")
print("[DEBUG] API KEY:", api_key)

print("✅ OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("✅ CLOVA_OCR_URL:", os.getenv("CLOVA_OCR_URL"))
print("✅ REPLICATE_API_TOKEN:", os.getenv("REPLICATE_API_TOKEN"))

client = OpenAI(api_key=api_key)


# 1. 맞춤법 교정
def correct_diary(raw_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 맞춤법 교정기야. 문장에서 맞춤법과 띄어쓰기를 고쳐줘. 설명하지 말고, 교정된 문장만 출력해."},
            {"role": "user", "content": raw_text}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


# 2. 그림에 넣을 시각 장면 요약
# def summarize_main_scene(corrected_text: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": (
#                 "You are a visual scene extractor for children's diary entries. "
#                 "Describe a single visually rich and coherent scene in English that best represents the diary entry. "
#                 "Focus only on drawable elements like people, actions, objects, and background."
#             )},
#             {"role": "user", "content": corrected_text}
#         ],
#         temperature=0.5
#     )
#     return response.choices[0].message.content.strip()
def summarize_main_scene(corrected_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a visual scene extractor for children's diary entries. "
                    "Read the diary entry in Korean, then imagine the most drawable scene from it. "
                    "Respond with only one English sentence that describes that scene in a visual and drawable way. "
                    # "Only respond with a single English sentence that describes the most drawable visual scene. "
                    "Do not include translation of the whole diary. Only output the drawable scene description."
                )
            },
            {
                "role": "user",
                "content": f"{corrected_text}"
            }
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


# 3. 화풍 프롬프트 템플릿
style_prompt_map = {
    "만화같이": (
        "Create a 3D animated illustration for a children's diary in the style of Pixar or Disney. "
        "Use soft lighting, stylized 3D cartoon characters, and a warm atmosphere. "
        "The visual style should resemble animated movie scenes with vivid colors and expressive facial features."
    ),
    "수채화": (
        "Create a watercolor-style illustration for a children's diary. "
        "Use flowing brushstrokes, soft pastel colors, and a gentle tone. "
        "The image should feel light, warm, and whimsical, like a page from a picture book."
    ),
    "유화": (
        "Create an illustration for a children's diary in the style of Vincent van Gogh. "
        "Use expressive and swirling brush strokes, bold color contrasts, and thick texture to mimic Van Gogh's oil painting technique. "
        "The scene should feel emotional and lively, with stylized characters and scenery. "
        "Avoid realism—emphasize painterly abstraction, especially in the sky and background elements, evoking a dreamy and energetic atmosphere."
    ),
    "몽환적인": (
        "Create a dreamy and magical cartoon-style illustration for a children's diary. "
        "Use soft pastel tones, glowing lights, and a warm, whimsical atmosphere. "
        "Include stylized cute characters with round features and large eyes, like those in children's fantasy picture books. "
        "The scene should feel surreal but playful, with a soft, childlike charm."
    ),
    "배경중심": (
        "Create a background-focused illustration for a children's diary. "
        "Do not include any characters. "
        "Emphasize the overall mood, lighting, and color harmony of the environment to tell the story visually."
    )
}


# 4. 색감 프롬프트 템플릿
# color_prompt_map = {
#     "빨간색": "Use vivid red tones as the dominant color throughout the scene.",
#     "주황색": "Use a warm orange palette to bring energy and brightness to the image.",
#     "노랑색": "Use cheerful yellow tones to create a bright and sunny mood.",
#     "초록색": "Use fresh green colors to reflect a lively and natural atmosphere.",
#     "하늘색": "Use light blue hues to create a peaceful and open feeling.",
#     "보라색": "Use soft purple tones to convey calm and creativity.",
#     "분홍색": "Use cute pink colors to give a playful and lovely tone to the scene."
# }
color_prompt_map = {
    "화남": "Use vivid red tones as the dominant color throughout the scene. Emphasize intensity and passion with strong highlights and bold contrasts.",
    "놀라움": "Use a warm orange palette to bring energy and brightness to the image. Incorporate sudden lighting or dynamic elements to enhance the surprise.",
    "기쁨": "Use cheerful yellow tones to create a bright and sunny mood. Ensure the overall atmosphere feels uplifting, with soft shadows and golden highlights.",
    "활기찬": "Use fresh green colors to reflect a lively and natural atmosphere. Include vibrant greenery or bright lighting to emphasize vitality and movement.",
    "슬픔": "Use light blue hues to create a peaceful and open feeling. Utilize soft gradients and subtle light to express a calm and melancholic mood.",
    "신비로움": "Use soft purple tones to convey calm and creativity. Blend lavender and twilight shades to evoke a mysterious and imaginative ambiance.",
    "무난": "Use warm beige tones to give a soft, cozy, and elegant feeling to the scene. Maintain a balanced and neutral look with gentle highlights and smooth textures."
}


# 5. 캐릭터 설정
def get_character_prompt(gender: str, use_custom: bool, hairstyle: str = "", outfit: str = "") -> str:
    if not use_custom:
        default_map = {
            "girl": (
                "The main character is a young girl with a round face, short straight black hair, and expressive dark brown eyes. "
                "She is wearing a white top and a blue skirt. Her appearance should remain consistent."
            ),
            "boy": (
                "The main character is a young boy with a round face, short black hair, and big bright eyes. "
                "He is wearing a blue shirt and dark shorts. His appearance should remain consistent."
            )
        }
        return default_map[gender]

    # Custom
    if gender == "girl":
        hair_map = {
            "long": "long black hair",
            "med": "medium-length black hair",
            "short": "short black hair"
        }
        outfit_map = {
            "one": "a navy skirt and a white blouse",
            "two": "blue jeans and a pink short-sleeved shirt",
            "three": "a blue dress"
        }
    elif gender == "boy":
        hair_map = {
            "short": "short black hair"
        }
        outfit_map = {
            "four": "blue pants and a white shirt",
            "five": "beige shorts and a sky blue shirt"
        }
    else:
        raise ValueError(f"Invalid gender value: {gender}")

    # 방어적 접근
    hair_description = hair_map.get(hairstyle)
    outfit_description = outfit_map.get(outfit)

    if not hair_description or not outfit_description:
        raise ValueError(f"Invalid hairstyle or outfit: hairstyle={hairstyle}, outfit={outfit}")

    return (
        f"The main character is a young {gender} with {hair_description}, a round face, and expressive eyes. "
        f"They are wearing {outfit_description}. Their appearance should remain consistent throughout the illustration."
    )



# 6. 전체 프롬프트 조합
# def build_diary_prompt(scene: str, style: str, color: str, character_prompt: str) -> str:
#     style_part = style_prompt_map[style]
#     color_part = color_prompt_map.get(color, "")
#     return (
#         f"{style_part} {color_part}\n\n"
#         f"{character_prompt}\n\n"
#         f"Depict the following scene from the diary: {scene}\n\n"
#         f"Only include visual elements from the diary entry. No text in the image. "
#         f"Keep the mood bright, friendly, and child-appropriate."
#     )

def build_diary_prompt(scene: str, style: str, color: str, character_prompt: str) -> str:
    style_part = style_prompt_map[style]
    color_part = color_prompt_map.get(color, "")
    
    prompt_parts = [style_part, color_part.strip()]

    # 배경중심 스타일이 아닐 경우에만 캐릭터 프롬프트 포함
    if style != "배경중심":
        prompt_parts.append(character_prompt.strip())

    prompt_parts.append(
        f"Depict the following scene from the diary: {scene}\n\n"
        f"Only include visual elements from the diary entry. No text in the image. "
        f"Keep the mood bright, friendly, and child-appropriate."
    )

    return "\n\n".join([part for part in prompt_parts if part])