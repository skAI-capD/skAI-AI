# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)
# #걍 추가
# # 7. 이미지 생성
# def generate_diary_image(prompt: str) -> str:
#     response = client.images.generate(
#         model="dall-e-3",
#         prompt=prompt,
#         size="1024x1024",
#         quality="standard",
#         response_format="url"
#     )
#     return response.data[0].url

import os
import asyncio
import replicate
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 각 모델 호출 함수
def generate_with_dalle(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="url"
    )
    return response.data[0].url

def generate_with_blackforest(prompt: str) -> str:
    try:
        output = replicate.run(
            "black-forest-labs/flux-kontext-pro",
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "output_format": "jpg"
            }
        )
        return str(output)
    except Exception as e:
        print("[ERROR] BlackForest 이미지 생성 실패:", e)
        return "error_blackforest" 


def generate_with_sd(prompt: str, negative_prompt: str = "") -> str:
    output = replicate.run(
        "stability-ai/stable-diffusion-3.5-large", 
        input={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30
        }
    )
    return str(output[0])

# 병렬 실행
def generate_all_images(prompt: str) -> dict:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def gather_results():
        return await asyncio.gather(
            loop.run_in_executor(None, generate_with_dalle, prompt),
            loop.run_in_executor(None, generate_with_sd, prompt),
            loop.run_in_executor(None, generate_with_blackforest, prompt)
        )

    dalle_url, sd_url, bfl_url = loop.run_until_complete(gather_results())
    return {
        "DALL·E 3": dalle_url,
        "Stable Diffusion": sd_url,
        "Black Forest Lab": bfl_url
    }