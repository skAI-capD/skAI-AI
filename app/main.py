from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.ocr_utils import extract_text_from_image
from app.pipeline import run_diary_image_pipeline

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-diary-image")
async def generate_diary_image_api(
    diaryImage: UploadFile = File(...),
    gender: str = Form(...),
    style: str = Form(...),
    color: str = Form(...),
    useCustom: bool = Form(...),
    hairstyle: str = Form(""),
    outfit: str = Form("")
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
            "imageUrl": result["imageUrl"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
