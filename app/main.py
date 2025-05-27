from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.ocr_utils import extract_text_from_image
from app.pipeline import run_diary_image_pipeline

app = FastAPI()

# CORS 허용 (프론트에서 직접 호출 시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-diary-image")
async def generate_diary_image_api(
    diaryImage: Optional[UploadFile] = File(None),
    diaryText: Optional[str] = Form(None),
    gender: str = Form(...),
    style: str = Form(...),
    color: str = Form(...),
    useCustom: bool = Form(...),
    hairstyle: str = Form(""),
    outfit: str = Form("")
):
    try:
        # 1. 이미지 or 텍스트 선택 처리 (방어적 체크 포함)
        if diaryImage and hasattr(diaryImage, "file") and getattr(diaryImage, "filename", ""):
            original = extract_text_from_image(diaryImage)
        elif diaryText:
            original = diaryText
        else:
            return JSONResponse(status_code=400, content={"error": "텍스트 또는 이미지 중 하나는 반드시 필요합니다."})


        # 2. 파이프라인 실행
        result = run_diary_image_pipeline(
            diary_text=original,
            gender=gender,
            style=style,
            color=color,
            use_custom=useCustom,
            hairstyle=hairstyle,
            outfit=outfit
        )

        # 3. 최종 응답
        return {
            "originalText": original,
            "correctedText": result["correctedText"],
            "imageUrl": result["imageUrl"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
