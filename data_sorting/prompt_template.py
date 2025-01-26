PROMPT_TEMPLATE = """You are given a JSON object describing a product from an e-commerce site.

For example:
{
  "big_category": "아우터",
  "sub_category": "무스탕/퍼",
  "gender": "여",
  "season": "FW",
  "product_name": "시어링 자켓 블랙 ZG6MU605BK",
  "image_url": "..."
}

Your goal:

1. Read the "product_name" field (e.g. "시어링 자켓 블랙 ZG6MU605BK").

2. Remove any meaningless product code or model number that consists of random letters/digits 
   (for example "ZG6MU605BK", "AB1234", or "MUS2023X" etc.).
   - Typically these codes are uppercase letters/numbers with length >= 5.
   - If it’s obviously a brand or short acronym (like "UNIQ", "FW23"), do not remove if it's obviously not a random code.
   - Use your best judgment.

3. After removing such codes, parse the cleaned product_name to extract:
   - "color": color references (ex. "블랙", "핑크", "ivory", "brown", "민트", etc.)
   - "material": words describing the fabric/material (ex. "무스탕", "레더", "가죽", "퍼", "시어링", "울", "코듀로이" etc.)
   - "feature": other descriptive keywords (ex. "워싱", "크롭", "오버핏", "후드", "자켓", "코트", "하이넥" etc.)

   - If multiple colors exist, separate them by comma (e.g. "블랙, 아이보리").
   - If multiple materials or features exist, also separate them by comma.

4. If something doesn't exist, put an empty string "".

5. Finally, return the ENTIRE JSON object with three extra keys: "color", "material", and "feature", 
   and update the "product_name" by removing the product code substring(s).

   For example, if input is:
   {
     "big_category": "아우터",
     "sub_category": "무스탕/퍼",
     "gender": "여",
     "season": "FW",
     "product_name": "시어링 자켓 블랙 ZG6MU605BK",
     "image_url": "..."
   }

   We want an output like:
   {
     "big_category": "아우터",
     "sub_category": "무스탕/퍼",
     "gender": "여",
     "season": "FW",
     "product_name": "시어링 자켓 블랙",
     "color": "블랙",
     "material": "시어링",
     "feature": "자켓",
     "image_url": "..."
   }

Important details:
- Keep all original keys and values the same, except for "product_name" from which you remove the product code substring(s).
- color/material/feature should be comma-separated if multiple.
- If no color/material/feature is found, just keep them as "".
- Do not remove or rename existing keys other than cleaning up "product_name".
- Output must be valid JSON.
"""
