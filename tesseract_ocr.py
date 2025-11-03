from PIL import Image
import pytesseract
from result_compare import calculate_accuracy
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def tesseract_ocr_result(image_path, original_text):
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image, lang='eng')
    accuracy = calculate_accuracy(original_text, ocr_text)

    print("\n"+"="*80+"\n")
    print(f"OCR 인식률: {accuracy:.2f}%\n")
    print("원본 텍스트: ")
    print(f"{original_text}")
    print("OCR 결과: \n")
    print(f"{ocr_text}")

    return accuracy

# original_texts = [
#     """
# This is a hdanwritten
# example
# write as good as you can
#     """,
#     """
# I live in Lviv.
# Every day I go
# to work by bus.
# Also I would
# like to visit Hars
#     """
# ]

hdanwritten1_original_text = """
This is a hdanwritten
example
write as good as you can
"""

hdanwritten2_original_text = """
I live in Lviv.
Every day I go
to work by bus.
Also I would
like to visit Hars
"""

# accuracy1 = tesseract_ocr_result("./images/handwritten1.png", original_texts[0])
accuracy1 = tesseract_ocr_result("./images/handwritten1.png", hdanwritten1_original_text)
# accuracy2 = tesseract_ocr_result("./images/handwritten2.png", original_texts[1])
accuracy2 = tesseract_ocr_result("./images/handwritten2.png", hdanwritten2_original_text)


# 결과 폴더 생성
result_dir = './result'
os.makedirs(result_dir, exist_ok=True)

# Nanum 폰트 설정 (한글 지원)
font_path = '../11-03/NanumGothicLight.ttf'
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

# 두 이미지의 결과를 리스트로 저장
image_names = ['handwritten1', 'handwritten2']
accuracies = [accuracy1, accuracy2]  # 아래에서 값 지정됨

# 그래프
plt.bar(image_names, [accuracy1, accuracy2], color='skyblue')
plt.title("OCR 인식률 비교")
plt.xlabel("이미지 이름")
plt.ylabel("인식률 (%)")
plt.ylim(0, 100)


# 막대 위에 수치 표시
for i, acc in enumerate(accuracies):
    plt.text(i, acc + 1, f"{acc:.2f}%", ha='center', fontsize=10)

# 결과 저장
output_path = os.path.join(result_dir, 'tesseract_result.png')
plt.savefig(output_path, dpi=200, bbox_inches='tight')
plt.close()  # 메모리 절약
print(f"그래프가 {output_path} 에 저장되었습니다.")