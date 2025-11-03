import fitz  # PyMuPDF
from PIL import Image
from result_compare import calculate_accuracy
import pytesseract
import io
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def extract_text_from_pdf(pdf_path):
   doc = fitz.open(pdf_path)
   full_text = ""

   for page_num in range(len(doc)):
       page = doc.load_page(page_num)
       text = page.get_text()
       full_text += text

       # 이미지 추출
       image_list = page.get_images()
       for img_index, img in enumerate(image_list):
           xref = img[0]
           base_image = doc.extract_image(xref)
           image_bytes = base_image["image"]
           img_pil = Image.open(io.BytesIO(image_bytes))

           # OCR 수행하여 이미지 내 텍스트 추출
           img_text = pytesseract.image_to_string(img_pil, lang='kor')
           full_text += "\n[이미지 내 텍스트]\n" + img_text + "\n"

   return full_text

original_text1 = """
김병직
형?
2016학년도 연세대 논술- 인문계열
[문제 1] 예술적 성취에 대한 제시문 (가), (나), (다)의 논지를 비교, 분석하시오. (1,000자 안팎, 50점)
[문제 2/제시문 (라)를 바탕으로 제시문 (가), (나), (다)의 논지를 평가하시오. (1,000자 안팎, 50점)
2016학년도 연세대 논술- 사회계열
[문제 1] 제시문 (가), (나), (다)는 '진정성 있는 사람'에 대한 서로 다른 관점을 보여준다.
이 세 가지 관점의 차이를 설명하시오. (1,000자 안팎. 50점)
[문제 2] 제시문 (라)의 <그림 1>과 〈그림 2>에 나타난 특징들을 분석하고, 이를 제시문 (가)와 (나)에 근거하여 해석하시오. (1,000자 안팎, 50점)
2016학년도 서울시립대 논술
[문항 1] 제시문 (가)의 주장을 250자 내외로 요약한 뒤, 주된 견해나 관점이 (가)와 다른 제시문을 (나)~(라)에서 모두 찾아 (가]와 각각 어떻게 차이가 나는지 구체적으로 밝히시오. (600자 내외, 배점 30점) 
[문항 2]<그림 1>과 <그림 2>를 근거로 마리엘리토의 유입이 마이애미 노동시장에 미친 영향을 추론하시오.
단, 그러한 추론을 위해 필요한 가정(들)을 반드시 포함하여 서술하시오. (400자 내외, 배점 20점)
[문항 3]<보기>에 나타난 A씨의 태도에 찬성하는지 혹은 반대하는지 어느 한 입장을 정한 뒤, [개)~[라]의 모든 제시문을
활용하되 주된 견해나 관점이 자신의 입장과 같은 제시문의 논거는 지지하고 자신의 입장과 다른 제시문의 논거는 비판하면
서 자신의 입장을 옹호하시오. (1,000자 내외, 배점 50점)
2016학년도 동국대 논술
[문제 1] 제시문 [가]와 [나]를 참고로 하여, '남녀 대화의 대표적 특성'을 변화시킬 수 있는 요인에 대해 서술하시오.
11~12줄 (330~360자) [30점)
[문제 2] 제시문 [가]와 [나]의 핵심어를 찾아 맥락상의 공통적인 주장을 기술하시오. 8~9출 (240~270자) [30점] 
[문제 3] 제시문 [다], [라], [마], [바]를 시대 순에 따라 배열하여 민주주의의 발전 과정을 요약하시오.
그리고 제시문 [라]를 참고하여 시민운동의 구체적인 사례를 제시하고
그것이 민주주의 발전에 끼친 긍정적 영향에 대해 기술하시오. 22~23 (660~690자) [40점]
2016학년도 홍익대 논술
[문제 1] 제시문 (가)에서 문자 문화의 특성을 찾아 요약하고, 이를 바탕으로 (나), (다), (라)에 나타난 독서 경험이나
책에 대한 태도를 분석하여 논술하시오. (800± 100자) 
[문과대학, 사범대학 및 예술학과 지원자에게는 타 문제의 2배의 배점]
[문제 2] 제시문 (마)와 (바)의 주요 개념이 (사), (아), (자)에 각각 어떻게 적용될 수 있는지 논술하시오. (800 ±100자)
[경영대학, 경제학부 및 법학부 지원자에게는 타 문제의 2배의 배점]
2016학년도 경기대 논술
[문항 1] 나의 ㄱ에 대한 문제 해결책으로서 가 작품에 대해 설명하고, 그것의 한계를 다를 통해 논술하시오. (700± 50자)
[문항 2] 가의 쓰레기 종량세가 사회 제도로서 가지는 의의를 나의 관점에서 설명하고.
이 제도가 이전의 제도에 비해 효과적이었던 까닭을 다에 제시된 소비의 특성을 활용하여 논술하시오. (700 ±50자)
"""

# 사용 예:
pdf_text = extract_text_from_pdf("./pdfs/pyMuPDF_sample_pdf.pdf")

accuracy = calculate_accuracy(original_text1, pdf_text)
print(f"\nPDF 인식률: {accuracy:.2f}%\n")

print("PDF 원본 텍스트:\n")
print(original_text1)

print("PDF 텍스트 및 이미지 내 텍스트:\n")
print(pdf_text)

result_dir = './result'
os.makedirs(result_dir, exist_ok=True)

# 한글 폰트 등록
font_path = '../11-03/NanumGothicLight.ttf'
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothic')

# 막대그래프
plt.bar(['PyMuPDF OCR 결과'], [accuracy], color='teal')
plt.title("PyMuPDF 텍스트 인식률 결과")
plt.ylabel("인식률 (%)")
plt.ylim(0, 100)
plt.text(0, accuracy + 1, f"{accuracy:.2f}%", ha='center', fontsize=10)

# 결과 저장
output_path = os.path.join(result_dir, 'pyMuPDF_result.png')
plt.savefig(output_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"그래프가 '{output_path}'에 저장되었습니다.")