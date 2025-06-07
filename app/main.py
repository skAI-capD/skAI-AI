from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.ocr_utils import extract_text_from_image
from app.pipeline import run_diary_image_pipeline
import nest_asyncio
nest_asyncio.apply()


app = FastAPI(
    title="Diary API",
    docs_url="/docs",  # ✅ 이게 있어야 Swagger 접근 가능
    redoc_url=None
)
import os
from dotenv import load_dotenv  
load_dotenv()  

print("✅ MAIN - OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/dictation-ocr")
async def extract_text_for_dictation(image: UploadFile = File(...)):
    try:
        print("[DEBUG] API KEY:", os.getenv("OPENAI_API_KEY"))

        if not image or not hasattr(image, "file") or not image.filename:
            return JSONResponse(status_code=400, content={"error": "이미지는 필수입니다."})

        extracted_text = extract_text_from_image(image)

        return {
            "extractedText": extracted_text or ""
        }

    except Exception as e:
        print("[ERROR] OCR 처리 중 예외:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/generate-diary-image")
async def generate_diary_image_api(
    diaryImage: UploadFile = File(...),
    gender: str = Form(...),
    style: str = Form(...),
    color: str = Form(...),
    useCustom: bool = Form(...),
    hairstyle: str = Form(...),
    outfit: str = Form(...)
):
    try:
        # 이미지 필수 체크 및 OCR 수행
        if not diaryImage or not hasattr(diaryImage, "file") or not diaryImage.filename:
            return JSONResponse(status_code=400, content={"error": "이미지는 필수입니다."})

        original = extract_text_from_image(diaryImage)

        result = run_diary_image_pipeline(
            diary_text=original,
            gender=gender,
            style=style,
            color=color,
            use_custom=useCustom,
            hairstyle=hairstyle,
            outfit=outfit
        )

        return {
            "originalText": original,
            "correctedText": result["correctedText"],
            "imageUrls": result["imageUrls"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    print("[DEBUG] API KEY:", os.getenv("OPENAI_API_KEY"))  # 꼭 None 아닌지 확인

    print("✅ OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    print("✅ CLOVA_OCR_URL:", os.getenv("CLOVA_OCR_URL"))
    print("✅ REPLICATE_API_TOKEN:", os.getenv("REPLICATE_API_TOKEN"))
