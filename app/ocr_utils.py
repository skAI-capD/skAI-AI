import requests
import os
import uuid
import time
import json
from dotenv import load_dotenv

load_dotenv()

CLOVA_OCR_URL = os.getenv("CLOVA_OCR_URL")
CLOVA_OCR_SECRET = os.getenv("CLOVA_OCR_SECRET")

# 파일형 UploadFile 기준
def extract_text_from_image(image_file):
    image_bytes = image_file.file.read()
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    files = {
        'file': ('image.jpg', image_bytes, 'application/octet-stream'),
        'message': (None, json.dumps(request_json), 'application/json')
    }

    headers = {
        'X-OCR-SECRET': CLOVA_OCR_SECRET
    }

    response = requests.post(CLOVA_OCR_URL, headers=headers, files=files)
    result = response.json()

    try:
        return ' '.join([field['inferText'] for field in result['images'][0]['fields']])
    except Exception:
        return ""
