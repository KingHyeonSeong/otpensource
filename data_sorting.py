import os
import json
import openai
from dotenv import load_dotenv
from prompt_template import PROMPT_TEMPLATE

# 1) .env 파일 로드
load_dotenv()

# 2) 환경변수에서 OpenAI API Key 불러오기
openai.api_key = os.environ.get("OPENAI_API_KEY")

def transform_product_data(product_obj: dict) -> dict:
    """
    하나의 product_obj(JSON 객체)를 GPT에게 변환시킨 뒤,
    GPT의 응답을 JSON으로 파싱하여 리턴.
    """
    # 1) 프롬프트 생성
    prompt = PROMPT_TEMPLATE + "\n\n" + json.dumps(product_obj, ensure_ascii=False, indent=2)
    
    # 2) OpenAI ChatCompletion API 호출 
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are ChatGPT."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    
    # 3) 응답에서 콘텐츠 추출
    gpt_reply = response["choices"][0]["message"]["content"].strip()
    
    # 4) GPT가 돌려준 문자열이 JSON 포맷이라고 가정, 파이썬 dict로 변환
    try:
        transformed = json.loads(gpt_reply)
    except json.JSONDecodeError:
        print("JSON 파싱 실패. 원본 응답:", gpt_reply)
        transformed = product_obj  # 실패 시 원본 그대로 리턴하거나, 로깅 처리
    
    return transformed


def main():
    # 1) 원본 JSON 읽어오기
    input_file = "하의/트레이닝_조거팬츠.json"
    with open(input_file, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    # 2) 각 상품 정보를 GPT로 정제
    results = []
    for idx, product in enumerate(products):
        print(f"Processing item {idx+1}/{len(products)}...")
        transformed_product = transform_product_data(product)
        results.append(transformed_product)
    
    # 3) 결과 JSON 파일 저장
    output_file = "트레이닝_조거팬츠.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("정렬화 완료! 결과를 저장했습니다:", output_file)


if __name__ == "__main__":
    main()
