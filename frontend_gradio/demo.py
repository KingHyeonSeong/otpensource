import gradio as gr
import requests
import base64
from io import BytesIO
from PIL import Image

# ✅ FastAPI 서버 URL (ngrok 또는 로컬 서버 주소)
FASTAPI_URL = "https://a8d2-35-232-247-92.ngrok-free.app/"

def decode_base64_to_image(base64_string):
    """Base64 문자열을 이미지로 변환"""
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_bytes))
    return image

# ✅ FastAPI에서 최근 check_similarity 결과를 가져오는 함수
def fetch_latest_result():
    """FastAPI에서 가장 최근 업로드된 이미지의 check_similarity 결과 확인"""
    response = requests.get(f"{FASTAPI_URL}/get_last_check")
    if response.status_code == 200:
        return response.json()
    return None

def get_clothing_image(doc_id):
    response = requests.get(f"{FASTAPI_URL}/get_clothing_info/{doc_id}")
    if response.status_code == 200:
        data = response.json()
        return data.get("image_base64", "")
    return None

# ✅ 특정 옷 정보를 가져오는 함수
def get_clothing_info(doc_id):
    """FastAPI에서 특정 의류 정보를 가져오는 함수"""
    response = requests.get(f"{FASTAPI_URL}/get_clothing_info/{doc_id}")
    if response.status_code == 200:
        data = response.json()

        image = decode_base64_to_image(data.get("image_base64"))
        created_date = data.get("created_at", "")[:10]
        updated_date = data.get("updated_at", "")[:10]

        return (
            image,
            data.get("big_category", ""),
            data.get("sub_category", ""),
            data.get("gender", ""),
            data.get("season", ""),
            data.get("color", ""),
            data.get("material", ""),
            data.get("feature", ""),
            str(data.get("count", 0)),  
            created_date,
            updated_date,
            doc_id,
            gr.Row(visible=False),
            gr.Row(visible=True),
            gr.Row(visible=True)
        )
    return ("", "", "", "", "", "", "", "", "", "", None)

def update_clothing_info(doc_id, bigcategory, subcategory, gender, season, color, material, feature, count, first_date, last_date):
    """FastAPI를 통해 의류 데이터를 업데이트하는 함수"""
    update_data = {
        "big_category": bigcategory,
        "sub_category": subcategory,
        "gender": gender,
        "season": season,
        "color": color,
        "material": material,
        "feature": feature,
        "count": int(count), # 🔹 숫자로 변환
        "created_at": first_date,  
        "updated_at": last_date  # 🔹 최근 착용 날짜 업데이트
    }

    response = requests.put(f"{FASTAPI_URL}/update_clothing_info/{doc_id}", json=update_data)

    if response.status_code == 200:
        return f"✅ 업데이트 성공!"
    else:
        return "❌ 업데이트 실패, 다시 시도하세요."

# ✅ AI 모델 실행하여 새 옷 등록
def process_ai_model():
    response = requests.post(f"{FASTAPI_URL}/process_last_checked")

    if response.status_code == 200:
        new_id = response.json().get("doc_id")
        response = requests.get(f"{FASTAPI_URL}/get_clothing_info/{new_id}")
        if response.status_code == 200:
            data = response.json()

            image = decode_base64_to_image(data.get("image_base64"))
            created_date = data.get("created_at", "")[:10]
            updated_date = data.get("updated_at", "")[:10]

            return (
                "AI 모델 이미지 추출 완료",
                image,
                data.get("big_category", ""),
                data.get("sub_category", ""),
                data.get("gender", ""),
                data.get("season", ""),
                data.get("color", ""),
                data.get("material", ""),
                data.get("feature", ""),
                str(data.get("count", 0)),  
                created_date,
                updated_date,
                new_id,
                gr.Row(visible=False),
                gr.Row(visible=True),
                gr.Row(visible=True)
            )
        return ("", "", "", "", "", "", "", "", "", "", "", None)
    else:
        return {
            notify_box: "❌ AI 모델 실행 오류",
            yes_no_col: gr.Row(visible=False)
        }
    
# ✅ "데이터 수신" 버튼 클릭 시 실행
def check_clothing_data():
    """FastAPI에서 최신 유사한 의류 데이터를 확인하고 UI에 표시"""
    result = fetch_latest_result()

    if not result or not result.get("last_checked", False):
        return {
            notify_box: "⚠ 감지된 데이터가 없습니다.",
            poll_result: None,
            yes_no_col: gr.Row(visible=False),
            result_box: gr.Row(visible=False),
            modeling_col: gr.Row(visible=False),
            check_btn: gr.Row(visible=True)
        }  

    message = result.get("message", "⚠ 감지된 데이터가 없습니다.")
    clothing_id = result.get("existing_clothing_id", None)

    # 🔹 기존 옷이 존재할 경우 → "네/아니오" 버튼 활성화
    if clothing_id and clothing_id != "NEW_CLOTHING":
        return {
            notify_box: message,
            poll_result: clothing_id,
            yes_no_col: gr.Row(visible=True),
            result_box: gr.Row(visible=False),
            modeling_col: gr.Row(visible=False),
            check_btn: gr.Row(visible=False)
          }  # ✅ "네/아니오" 버튼 활성화

    return {
            notify_box: "기존과 유사한 의류 없음",
            poll_result: clothing_id,
            yes_no_col: gr.Row(visible=False),
            result_box: gr.Row(visible=False),
            modeling_col: gr.Row(visible=True),
            check_btn: gr.Row(visible=False)
          }

# ✅ FastAPI에서 모든 옷 정보를 불러오는 함수
def get_all_clothing():
    response = requests.get(f"{FASTAPI_URL}/get_all_clothing")
    if response.status_code == 200:
        data = response.json().get("clothes", [])
        images = []
        clothing_ids = []

        for item in data:
            if "image_base64" in item:
                images.append(decode_base64_to_image(item["image_base64"]))
                clothing_ids.append(item["_id"])  # ID 저장

        return images, clothing_ids  # ✅ 이미지 리스트와 ID 리스트 반환
    return [], []  # 데이터가 없을 경우 빈 리스트 반환

def load_closet():
    images, clothing_ids = get_all_clothing()
    if not images:
        return "❌ 옷장에 등록된 옷이 없습니다.", [], [], gr.Row(visible=False)
    
    return "📂 옷장 목록을 불러왔습니다.", images, clothing_ids, gr.Row(visible=True)


# ✅ 사용자가 갤러리에서 특정 옷을 클릭했을 때 실행할 함수
def select_clothing(evt: gr.SelectData, clothing_ids):
    index = evt.index
    if 0 <= index < len(clothing_ids):
        doc_id = clothing_ids[index]  # ✅ 선택한 옷의 ID 가져오기
        return get_clothing_info(doc_id)
    return None, "", "", "", "", "", "", "", "", "", "", ""

def delete_clothing():
    return gr.Row(visible=True), gr.Row(visible=True)

def delete_clothing_yes(doc_id):
    response = requests.delete(f"{FASTAPI_URL}/delete_clothing/{doc_id}")
    if response.status_code == 200:

        return (
            "✅ 삭제 완료! 정보 업데이트 필요.",
            gr.Row(visible=False),
            gr.Row(visible=False)
        )
    return ("", "", None)

def delete_clothing_no():
    return gr.Row(visible=False), gr.Row(visible=False)

# ✅ Gradio UI 구현
with gr.Blocks() as demo:
    with gr.Tab("옷 데이터 추가"):
        gr.Markdown("## 🏠 Otpensource")

        # 🔔 실시간 알림 메시지 박스
        notify_box = gr.Textbox(value="✅ 시스템 준비 완료!", label="🔔 알림 메시지", interactive=False)

        # ✅ "데이터 수신" 버튼
        check_btn = gr.Button("📡 데이터 수신")

        # ✅ 네/아니오 버튼 (기본적으로 숨김)
        with gr.Row(visible=False) as yes_no_col:
            yes_btn = gr.Button("✔️ 기존 의류(데이터 불러오기)")
            no_btn = gr.Button("❌ 새 의류(모델링 진행)")
        
        with gr.Row(visible=False) as modeling_col:
            modeling_btn = gr.Button("모델링 진행")

        with gr.Row(visible=False) as result_box:
            image_display = gr.Image(label="이미지 표시", interactive=False)
            with gr.Column():
                with gr.Row():
                    id = gr.Textbox(label="ID", interactive=False)
                with gr.Row():
                    bigcategory = gr.Textbox(label="큰 카테고리", interactive=True)
                    subcategory = gr.Textbox(label="작은 카테고리", interactive=True)
                with gr.Row():
                    gender = gr.Textbox(label="성별", interactive=True)
                    season = gr.Textbox(label="계절", interactive=True)
                with gr.Row():
                    color = gr.Textbox(label="색상", interactive=True)
                    material = gr.Textbox(label="소재/재질", interactive=True)
                with gr.Row():
                    feature = gr.Textbox(label="기타", interactive=True)
                with gr.Row():
                    first_date = gr.Textbox(label="구매일", interactive=True)
                    last_date = gr.Textbox(label="최근 사용일", interactive=True)
                with gr.Row():
                    count = gr.Textbox(label="착용 횟수", interactive=True)
                with gr.Row():
                    update_btn = gr.Button("💾 저장 (업데이트)")
                    delete_btn = gr.Button("❌ 삭제")
                with gr.Row(visible=False) as delete_box:
                    delete_alert = gr.Markdown(value="삭제하시겠습니까?")
                with gr.Row(visible=False) as delete_box2:
                    delete_yes_btn = gr.Button("✔️ 네")
                    delete_no_btn = gr.Button("❌ 아니오")


        # ✅ 결과 저장용 변수
        poll_result = gr.State(value=None)

        # ✅ "데이터 수신" 버튼 클릭 시 실행 (버튼 가시성 업데이트 추가)
        check_btn.click(
            fn=check_clothing_data,
            outputs=[notify_box, poll_result, yes_no_col, result_box, modeling_col, check_btn]
        )

        modeling_btn.click(
            fn=process_ai_model,
            outputs=[notify_box, image_display, bigcategory, subcategory, gender,
                      season, color, material, feature, count, 
                      first_date, last_date, id, modeling_col, result_box, check_btn]
        )

        # ✅ "네"를 선택하면 기존 데이터 가져오기
        yes_btn.click(
            fn=get_clothing_info,
            inputs=[poll_result],
            outputs=[image_display, bigcategory, subcategory, gender, season, 
                     color, material, feature, count, 
                     first_date, last_date, id, yes_no_col, result_box, check_btn]
        )

        # ✅ "아니오"를 선택하면 AI 모델 실행 후 새 옷 등록
        no_btn.click(
            fn=process_ai_model,
            outputs=[notify_box, image_display, bigcategory, subcategory, gender,
                      season, color, material, feature, count, 
                      first_date, last_date, id, yes_no_col, result_box, check_btn]
        )

        update_btn.click(
        fn=update_clothing_info,
        inputs=[id, bigcategory, subcategory, gender, season, color, material, feature, count, first_date, last_date],
        outputs=[notify_box]
        )

        delete_btn.click(
            fn=delete_clothing,
            outputs=[delete_box, delete_box2]
        )

        delete_yes_btn.click(
            fn=delete_clothing_yes,
            inputs=[id],
            outputs=[notify_box, delete_box, delete_box2]
        )

        delete_no_btn.click(
            fn=delete_clothing_no,
            outputs=[delete_box, delete_box2]
        )


    with gr.Tab("옷장 데이터 관리"):
        # 🔔 실시간 알림 메시지 박스
        notify_box2 = gr.Textbox(value="✅ 옷장 로드 준비 완료!", label="🔔 알림 메시지", interactive=False)
        
        load_btn = gr.Button("📂 내 옷장 불러오기")

        # ✅ 저장된 옷 ID 리스트 (사용자가 클릭했을 때 해당 ID 참조)
        clothing_ids_state = gr.State(value=[])

        with gr.Row(visible=False) as result_box2:
            # ✅ 갤러리 UI (이미지 목록 표시)
            gallery = gr.Gallery(label="👕 내 옷장", preview=True)
            with gr.Column():
                with gr.Row():
                    id = gr.Textbox(label="ID", interactive=False)
                with gr.Row():
                    bigcategory = gr.Textbox(label="큰 카테고리", interactive=True)
                    subcategory = gr.Textbox(label="작은 카테고리", interactive=True)
                with gr.Row():
                    gender = gr.Textbox(label="성별", interactive=True)
                    season = gr.Textbox(label="계절", interactive=True)
                with gr.Row():
                    color = gr.Textbox(label="색상", interactive=True)
                    material = gr.Textbox(label="소재/재질", interactive=True)
                with gr.Row():
                    feature = gr.Textbox(label="기타", interactive=True)
                with gr.Row():
                    first_date = gr.Textbox(label="구매일", interactive=True)
                    last_date = gr.Textbox(label="최근 사용일", interactive=True)
                with gr.Row():
                    count = gr.Textbox(label="착용 횟수", interactive=True)
                with gr.Row():
                    update_btn = gr.Button("💾 저장 (업데이트)")
                    delete_btn = gr.Button("❌ 삭제")
                with gr.Row(visible=False) as delete_box:
                    delete_alert = gr.Markdown(value="삭제하시겠습니까?")
                with gr.Row(visible=False) as delete_box2:
                    delete_yes_btn = gr.Button("✔️ 네")
                    delete_no_btn = gr.Button("❌ 아니오")
        

        load_btn.click(
        fn=load_closet,
        outputs=[notify_box2, gallery, clothing_ids_state, result_box2]
        )

        # ✅ 사용자가 갤러리에서 옷을 선택하면 상세 정보 표시
        gallery.select(
        fn=select_clothing,
        inputs=[clothing_ids_state],
        outputs=[image_display, bigcategory, subcategory, gender, season, 
                 color, material, feature, count, first_date, last_date, 
                 id, yes_no_col, result_box2, load_btn]
        )

        update_btn.click(
        fn=update_clothing_info,
        inputs=[id, bigcategory, subcategory, gender, season, color, material, feature, count, first_date, last_date],
        outputs=[notify_box2]
        )

        delete_btn.click(
            fn=delete_clothing,
            outputs=[delete_box, delete_box2]
        )

        delete_yes_btn.click(
            fn=delete_clothing_yes,
            inputs=[id],
            outputs=[notify_box2, delete_box, delete_box2]
        )

        delete_no_btn.click(
            fn=delete_clothing_no,
            outputs=[delete_box, delete_box2]
        )

# ✅ Gradio 실행
demo.launch(debug=True, share=True)