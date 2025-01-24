import os
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 인자로 max_items를 추가하여 크롤링할 상품 개수를 제한할 수 있음
def crawl_musinsa_category(category_url, scroll_count=30, max_items=200):
    """
    무신사 특정 카테고리 페이지에서
    스크롤을 일정 횟수 내려 상품들을 크롤링하고,
    각 상품의 상세페이지 URL을 모아서 리턴.
    """
     # 1) 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("headless")  # 헤드리스 모드(창 안 띄우기)

    # 2) 크롬 실행 (창이 뜨지 않음)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(category_url)
    #time.sleep(1)

    detail_links = []

    for _ in range(scroll_count):
        # 스크롤 내리기
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        #time.sleep(1)

        # 스크롤 후 페이지소스 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 현재까지 로드된 상품 a태그들
        product_items = soup.select('a.sc-eldOKa.eYuOFs.gtm-view-item-list.gtm-select-item')
        
        for item in product_items:
            href = item.get('href', '')
            if href:
                # 절대경로 처리
                if href.startswith("http"):
                    link = href
                else:
                    link = "https://www.musinsa.com" + href

                # detail_links에 중복되지 않게 추가
                if link not in detail_links:
                    detail_links.append(link)

                    # 이미 max_items개면 즉시 중단
                    if len(detail_links) >= max_items:
                        break
        
        # 만약 이미 max_items개를 모았다면 스크롤 더 안 내려도 되므로 break
        if len(detail_links) >= max_items:
            break

    driver.quit()
    return detail_links


def crawl_musinsa_product_detail(product_url):
    """
    무신사 상품 상세 페이지에 접속하여
      - image_url
      - big_category 
      - sub_category
      - gender
      - season (년도 제외)
      - product_name
    만 크롤링해서 딕셔너리로 리턴.
    """
     # 1) 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("headless")  # 헤드리스 모드(창 안 띄우기)

    # 2) 크롬 실행 
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(product_url)
    #time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # (1) 세부 카테고리 (2depth)
    sub_cat_tag = soup.select_one('a[data-button-name="상품카테고리"][data-category-id="2depth"]')
    if sub_cat_tag and sub_cat_tag.has_attr('data-category-name'):
        sub_category = sub_cat_tag['data-category-name']
    else:
        sub_category = ""

    # (2) 제품명
    product_name_tag = soup.find("span", class_="text-lg font-medium break-all flex-1 font-pretendard")
    product_name = product_name_tag.get_text(strip=True) if product_name_tag else ""

    # (3) 이미지 URL
    img_tag = soup.select_one('img.sc-8j14dt-8.ljkZhU')
    if img_tag:
        image_url = img_tag.get('src', '')
    else:
        fallback_tag = soup.find('img', alt=True)
        image_url = fallback_tag['src'] if fallback_tag else ""

    # (4) 성별
    gender = ""
    gender_dt = soup.find("dt", string="성별")
    if gender_dt:
        gender_dd = gender_dt.find_next_sibling("dd")
        if gender_dd:
            gender = gender_dd.get_text(strip=True)

    # (5) 시즌 (년도 제외)
    season = "정보 없음"
    season_dt = soup.find("dt", string="시즌")
    if season_dt:
        season_dd = season_dt.find_next_sibling("dd")
        if season_dd:
            season_text = season_dd.get_text(separator=" ", strip=True)
            # 정규식으로 F/W, S/S, FW, SS, AW, A/W 등을 찾음
            pattern = re.compile(r"(?:S/S|F/W|SS|FW|A/W|AW)", re.IGNORECASE)
            matches = pattern.findall(season_text)
            if matches:
                season = matches[0].upper()
            else:
                season = "정보 없음"

    driver.quit()

    product_data = {
        "big_category": "",         
        "sub_category": sub_category,
        "gender": gender,
        "season": season,
        "product_name": product_name,
        "image_url": image_url
    }

    return product_data


def main():
    # 여기서 big_category를 아우터/상의/하의/원피스 중 선택, 그리고 카테고리 링크는 sub_category
    category_urls = {
        "아우터": "https://www.musinsa.com/category/002025?gf=A", # 무스탕/퍼
        # "상의": "카테고리 링크",
        # "하의": "카테고리 링크",
        # "원피스/스커트": "카테고리 링크",
    }

    all_data = []

    for cat_name, cat_url in category_urls.items():
        print(f"=== Start crawling category: {cat_name} ===")
        # scroll_count 원하는 만큼 설정
        detail_links = crawl_musinsa_category(cat_url, scroll_count=30)
        print(f"Found {len(detail_links)} product links in {cat_name}")

        for link in detail_links:
            try:
                product_info = crawl_musinsa_product_detail(link)
                product_info["big_category"] = cat_name  # 카테고리 이름 할당
                all_data.append(product_info)
            except Exception as e:
                print(f"Error on link: {link}, {e}")
    
    # 폴더 "아우터" 안에 JSON 파일 저장
    # (아우터 폴더를 미리 생성)
    file_path = os.path.join("아우터", "무스탕_퍼.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print("크롤링 완료! JSON 파일로 저장.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"총 실행 시간: {end_time - start_time:.2f}초")