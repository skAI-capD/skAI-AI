from pydantic import BaseModel
from typing import Optional

class DiaryInput(BaseModel):
    diaryText: Optional[str] = None  # 이미지와 텍스트 중 하나 필수
    gender: str
    style: str
    color: str
    useCustom: bool
    hairstyle: Optional[str] = ""
    outfit: Optional[str] = ""

class DiaryOutput(BaseModel):
    originalText: str
    correctedText: str
    imageUrl: str
