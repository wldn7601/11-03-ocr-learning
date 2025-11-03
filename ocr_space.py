import requests
import json
from result_compare import calculate_accuracy
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -----------------------------
# 환경 변수 로드
# -----------------------------
load_dotenv()
api_key = os.getenv("OCR_SPACE_API_KEY")

# -----------------------------
# OCR.Space API 호출 함수
# -----------------------------
def ocr_space_api(image_path, api_key, language):
    url_api = "https://api.ocr.space/parse/image"
    with open(image_path, 'rb') as f:
        response = requests.post(
            url_api,
            files={"filename": f},
            data={"apikey": api_key, "language": language},
            timeout=30
        )
    result = response.json()
    parsed = result.get("ParsedResults")
    return parsed[0].get("ParsedText", "")

# -----------------------------
# OCR 비교 및 결과 출력 함수
# -----------------------------
def evaluate_ocr(image_path, original_text, api_key, language):
    text_result = ocr_space_api(image_path, api_key, language)
    accuracy = calculate_accuracy(original_text, text_result)

    print("\n"+"="*80+"\n")
    print(f"OCR SPACE 인식률: {accuracy:.2f}%\n")
    print("원본 텍스트:\n")
    print(original_text.strip())
    print("\nOCR 결과:\n")
    print(text_result.strip())
    return accuracy

# -----------------------------
# 테스트 데이터
# -----------------------------
cases = [
    {
        "image": "./images/identification_card.png",
        "text": """
주민등록증
이영희
780526-2345678
서울특별시 송파구 법원로11길
11, B동 610호
2020.12.25
서울특별시 송파구청장
""",
        "lang": "kor"
    },
    {
        "image": "./images/handwritten2.png",
        "text": """
I live in Lviv.
Every day I go
to work by bus.
Also I would
like to visit Hars
""",
        "lang": "eng"
    }
]

# -----------------------------
# 전체 평가 수행
# -----------------------------
results = []
labels = []

for case in cases:
    acc = evaluate_ocr(case["image"], case["text"], api_key, case["lang"])
    results.append(acc)
    labels.append(os.path.basename(case["image"]))

# -----------------------------
# 그래프 저장
# -----------------------------
result_dir = './result'
os.makedirs(result_dir, exist_ok=True)

# 폰트 등록
font_path = '../11-03/NanumGothicLight.ttf'
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

plt.bar(labels, results, color='steelblue')
plt.title("OCR.Space API 인식률 비교")
plt.ylabel("인식률 (%)")
plt.ylim(0, 100)
for i, acc in enumerate(results):
    plt.text(i, acc + 1, f"{acc:.2f}%", ha='center', fontsize=10)

output_path = os.path.join(result_dir, 'ocr_api_result.png')
plt.savefig(output_path, dpi=200, bbox_inches='tight')
plt.close()

print(f"\n그래프가 '{output_path}'로 저장되었습니다.")
