# 👕 **옷픈소스 (Otpensource) - 스마트 옷장 AI 시스템**  

> **AI 기반 스마트 옷장 관리 솔루션**  
> **"옷장에 옷을 걸기만 하면 AI가 자동으로 분석! 이제 옷장을 열지 않아도 내 옷을 한눈에 확인하세요."**  

---

## 📌 **프로젝트 개요**  

**옷픈소스(Otpensource)**는 **AI 기반 패션 관리 시스템**으로, 사용자의 옷을 **자동으로 인식 및 분류**하고 **효율적으로 관리**할 수 있도록 돕는 스마트 옷장 서비스입니다.  

- **사용자가 옷을 걸면 AI가 자동 분석** → 카테고리, 색상, 재질, 패턴 감지  
- **Android 앱과 연동** → 모바일에서 옷장 정보 확인 및 관리  
- **Hugging Face에 직접 학습한 AI 모델 배포**  
- **패션 데이터셋 구축** → 데이터 기반 AI 모델 학습  

> 🏆 **궁극적인 목표:**  
> 👉 **스마트 옷장 + 패션 커뮤니티 + AI 기반 코디 추천**  

---

## ✨ **주요 기능**  

✅ **📷 AI 기반 옷 인식**  
  - **카메라로 촬영한 옷을 AI가 자동으로 분석** → 종류, 색상, 재질, 패턴 감지  
  - 자체 구축한 패션 데이터셋을 활용하여 **Hugging Face AI 모델 학습**  

✅ **📲 스마트 옷장 관리 (Android 연동)**  
  - Android 앱에서 **옷을 추가/삭제/수정** 및 **카테고리별 정렬 가능**  
  - AI 분석 데이터와 함께 **사이즈, 브랜드, 구매 정보 입력** 가능  

✅ **🎨 브랜드 & 패션 스타일 인식**  
  - **로고 및 디자인 패턴 분석**을 통한 브랜드 구분  
  - 사용자의 스타일을 분석하고 **맞춤형 패션 추천 제공**  

✅ **🛒 쇼핑몰 연동 & 스타일 추천**  
  - **AI가 패션 트렌드 분석** 후 맞춤형 스타일 추천  
  - 구매한 옷을 자동 등록하여 기존 옷장과 통합 관리  

✅ **👥 패션 커뮤니티 & 스타일 공유**  
  - 내 옷장을 공유하고 **다른 유저들과 코디 추천**  
  - 비슷한 체형/스타일을 가진 유저와 **패션 스타일 비교 가능**  

✅ **📊 옷장 통계 분석 & AI 패션 추천**  
  - AI가 사용자의 **옷장 데이터를 분석**하고 **스타일 인사이트 제공**  
  - 계절별 선호 스타일, 자주 입는 옷 추천  

---

## 🏗️ **프로젝트 아키텍처**  

1. 데이터 크롤링 및 AI 학습 파이프라인

<p align="center">
  <img src="sample_image\pipeline1.png" alt="Vision Model Example" width="700"/>
</p>


1. 안드로이드 앱 및 Frontend, Backend flow-chart

<p align="center">
  <img src="sample_image\pipeline2.png" alt="Vision Model Example" width="700"/>
</p>


✔ **Android 앱** → 사용자가 **옷을 관리**하고 AI 데이터를 확인하는 모바일 인터페이스  
✔ **FastAPI 백엔드** → AI 분석 요청 처리, 데이터 저장 및 관리  
✔ **MongoDB** → 유저 데이터 & 옷장 정보를 저장하는 NoSQL 데이터베이스  
✔ **AI Vision 모델** → 자체 학습한 모델이 **옷의 종류, 색상, 패턴 감지**  
✔ **Gradio 웹 UI** → 옷장 정보를 **웹 브라우저에서 조회 가능**  

---

## 🔧 **기술 스택**  

### **🛠 Backend**
- **torchvision** – 이미지 처리 및 딥러닝 모델 제공 (PyTorch)  
- **pymongo** – MongoDB와 파이썬을 연결하는 데이터베이스 드라이버  
- **scikit-learn** – 머신러닝 모델 학습 및 평가
- **fastapi** – 고성능 비동기 REST API 프레임워크  
- **uvicorn** – FastAPI 실행을 위한 경량 ASGI 서버  
- **pyngrok** – 로컬 서버를 외부에서 접속 가능하게 하는 터널링 도구  
- **nest-asyncio** – Jupyter 등에서 비동기 이벤트 루프 실행 지원  
- **pillow** – 이미지 처리 및 변환을 위한 라이브러리  
- **python-multipart** – FastAPI에서 파일 업로드를 지원하는 라이브러리  
- **pydantic** – 데이터 검증 및 설정 관리를 위한 데이터 모델링

### **🤖 AI Model**
- **unsloth** – 경량화된 LLM 파인튜닝 및 최적화
- **transformers** – 사전 학습된 NLP 모델 제공 (Hugging Face)  
- **torch** – PyTorch 기반 딥러닝 프레임워크  
- **datasets** – 대규모 데이터셋 로드 및 전처리 (Hugging Face)  
- **trl** – 강화 학습을 활용한 LLM 미세 조정 라이브러리 (Hugging Face)  

### **🌐 Frontend**
- **gradio** – 머신러닝 모델이나 데이터 처리 함수에 대한 웹 인터페이스 제공
- **requests** – HTTP 요청을 보내고 응답을 처리하는 라이브러리  
- **base64** – 바이너리 데이터를 Base64 형식으로 인코딩/디코딩하는 모듈  
- **io.BytesIO** – 메모리에서 파일처럼 데이터를 읽고 쓰는 버퍼 객체  

### **📡 데이터 크롤링**
- **Selenium** – 웹 브라우저 자동화  
- **BeautifulSoup4** – HTML 데이터 크롤링  
- **Requests** – HTTP 요청 라이브러리  
- **Pandas** – 데이터 정렬 및 처리  

### **📱 Android App**
- **agp** – Android Gradle Plugin, 안드로이드 프로젝트 빌드를 위한 플러그인  
- **junit** – Java 기반 단위 테스트 프레임워크  
- **material** – 구글 머티리얼 디자인 컴포넌트
- **activity** – 안드로이드 액티비티 생명주기 및 최신 API를 지원
- **constraintlayout** – 복잡한 UI를 효율적으로 구성할 수 있는 레이아웃 시스템  
- **retrofit** – REST API와 통신을 쉽게 할 수 있도록 도와주는 HTTP 클라이언트
- **visionCommon** – Google ML Kit Vision API의 공통 기능을 제공하는 라이브러리  
- **playServicesTasks** – Google Play Services의 비동기 작업 관리
- **segmentationSelfie** – Google ML Kit의 셀피 이미지 분할(Selfie Segmentation) 라이브러리  
- **playServicesMlkitSubjectSegmentation** – ML Kit의 피사체 분할(Subject Segmentation) 기능을 제공하는 라이브러리  

---

## 🎯 **Hugging Face 모델 & 데이터셋**  

### **👕 AI Vision Model**  
🔗 [otpensource-vision](https://huggingface.co/hateslopacademy/otpensource-vision)  
✅ 자체 학습한 **Vision-Language 모델**로, 옷의 종류, 색상, 패턴을 분석 가능  

### **📊 패션 데이터셋**  
🔗 [otpensource_dataset](https://huggingface.co/datasets/hateslopacademy/otpensource_dataset)  
✅ 무신사 크롤링 데이터를 기반으로 구축된 **패션 분석 특화 데이터셋**  

---

## 📥 **설치 및 실행 방법**  

### 1️⃣ **백엔드 (FastAPI 서버 실행)**  
```bash
git clone https://github.com/hateslopacademy/otpensource.git
cd otpensource/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2️⃣ **웹 UI 실행 (Gradio)**
```bash
cd otpensource/frontend
python demo.py
```
👉 브라우저에서 `http://localhost:7860` 접속  

---

## 📌 **사용 예시**  

### **👕 AI 분석 결과 예시**
```json
{
  "category": "트렌치코트",
  "gender": "여성",
  "season": "봄/가을",
  "color": "네이비",
  "material": "면",
  "feature": "클래식 디자인, 벨트 포함"
}
```


### 📡 **옷장 전체 데이터 조회**
bash
GET http://localhost:8000/get_all_clothing

```json
{
  "clothes": [
    "id": "67a0c950454c50b822b6a624",
    "big_category": "상의",
    "sub_category": "롱슬리브",
    "gender": "남",
    "season": "사계절",
    "color": "화이트",
    "material": "면",
    "feature": " 스트라이프",
    "image_base64": "/9j/4AAQSkZJRgABAAAD/4gHYSUNDX1AQEAAAAABtbn…",
    "embedding_vector": Array (512),
    "created_at": "2025-02-03T13:50:10.540+00:00",
    "updated_at": "2025-02-03T13:50:10.540+00:00",
    "count": 4
  ]
}
```

---

## 🎨 **프로젝트 화면 예시**  

### 📷 **안드로이드 카메라 App**  
<p align="center">
  <img src="sample_image\App.png" alt="Vision Model Example" width="200"/>
</p>

### 🏠 **Otepnsource (Gradio UI)**  
#### 기초 화면
<p align="center">
  <img src="sample_image\screenshot1.png" alt="Gradio UI Example" width="700"/>
</p>

#### 의류 데이터 감지 안내
<p align="center">
  <img src="sample_image\screenshot2.png" alt="Gradio UI Example" width="700"/>
</p>

#### 의류 모델링 결과 출력 및 수정
<p align="center">
  <img src="sample_image\screenshot3.png" alt="Gradio UI Example" width="700"/>
</p>

#### 기존 의류 데이터 불러오기 및 관리
<p align="center">
  <img src="sample_image\screenshot4.png" alt="Gradio UI Example" width="700"/>
</p>

---

## 📜 **라이선스**  
이 프로젝트는 `Apache-2.0` 라이선스를 따릅니다.  

---

## 📢 **기여 방법**  
🙌 **Pull Request & Issue 환영!**  
- 새로운 기능 제안  
- 버그 리포트  
- 문서 개선  

---

## 📞 **문의 & 피드백**  
- **이메일:** hateslop@gmail.com  

---
