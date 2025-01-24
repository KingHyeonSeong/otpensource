import os
import json
import re
import openai
from dotenv import load_dotenv
from prompt_template import PROMPT_TEMPLATE

# 1) .env 파일 로드
load_dotenv()

# 2) 환경변수에서 OpenAI API Key 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_json_object(gpt_reply: str) -> dict:
    """
    GPT 응답 문자열에서 JSON 부분만 추출하여
    dict 로 파싱해서 반환한다.
    만약 파싱 실패 시에는 빈 dict를 반환.
    """

    # 1) ```json ...``` 코드 펜스가 있는 경우, 안쪽 내용만 추출
    code_fence_pattern = r"```(?:json)?([\s\S]*?)```"
    matches = re.findall(code_fence_pattern, gpt_reply)
    if matches:
        json_str = matches[0].strip()
    else:
        json_str = gpt_reply

    # 2) 실제 JSON 오브젝트 부분만 파싱하기
    start_idx = json_str.find("{")
    end_idx = json_str.rfind("}")
    if start_idx == -1 or end_idx == -1:
        return {}

    json_str = json_str[start_idx : end_idx+1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}


def transform_product_data(product_obj: dict) -> dict:
    """
    하나의 product_obj(JSON 객체)를 GPT에게 변환시킨 뒤,
    GPT의 응답을 JSON(dict)으로 파싱하여 리턴.
    """
    # 1) 프롬프트 생성
    prompt = PROMPT_TEMPLATE + "\n\n" + json.dumps(product_obj, ensure_ascii=False, indent=2)
    
    # 2) OpenAI ChatCompletion API 호출 
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are ChatGPT."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    
    # 3) 응답에서 메시지 추출
    gpt_reply = response["choices"][0]["message"]["content"].strip()
    
    # 4) gpt_reply 문자열에서 JSON dict 추출
    parsed_dict = extract_json_object(gpt_reply)
    
    return parsed_dict


def main():
    # 1) 원본 디렉토리와 파일 가져오기
    input_dir = "아우터" 
    json_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    # 2) 각 파일 처리
    for json_file in json_files:
        input_path = os.path.join(input_dir, json_file)

        # JSON 파일 읽기
        with open(input_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        # 상품 정제
        results = []
        for idx, product in enumerate(products):
            print(f"Processing {json_file} - item {idx + 1}/{len(products)}...")
            transformed_product = transform_product_data(product)
            results.append(transformed_product)

        # 덮어쓰기 저장
        with open(input_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"{json_file} 처리 완료!")
        
    # # 1) 원본 JSON 읽어오기
    # input_file = "아우터/겨울_더블코트.json"
    # with open(input_file, "r", encoding="utf-8") as f:
    #     products = json.load(f)  

    # # 2) 각 상품 정보를 GPT로 정제
    # results = []
    # for idx, product in enumerate(products):
    #     print(f"Processing item {idx+1}/{len(products)}...")
    #     transformed_product = transform_product_data(product)
    #     results.append(transformed_product)
    
    # # 3) 결과 JSON 파일 저장
    # output_file = "아우터/겨울_더블코트.json"
    # with open(output_file, "w", encoding="utf-8") as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
    
    # print("정제 완료! 결과 저장:", output_file)


if __name__ == "__main__":
    main()
