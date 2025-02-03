import requests
import datetime
import numpy as np
import torch
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from bson import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPModel, CLIPProcessor

client = MongoClient("mongodb://localhost:27017/")
db = client["otpensource"]
clothes_col = db["clothes"]

model_name = "openai/clip-vit-base-patch32"
device = "cpu"
print(f"[INFO] Loading CLIP model: {model_name} on device={device}")
clip_model = CLIPModel.from_pretrained(model_name).to(device)
clip_processor = CLIPProcessor.from_pretrained(model_name)

def get_clip_image_embedding(image_url: str):
    headers = {"User-Agent":"Mozilla/5.0"}
    resp = requests.get(image_url, timeout=10, headers=headers)
    resp.raise_for_status()
    pil_img = Image.open(BytesIO(resp.content)).convert("RGB")

    inputs = clip_processor(images=pil_img, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = clip_model.get_image_features(**inputs)  # shape (1,512)
    embedding = outputs[0].cpu().numpy()
    return embedding.tolist()  # list of float

def find_most_similar_embedding(new_embedding, threshold=0.9):
    docs = list(clothes_col.find({"embedding_vector": {"$exists": True, "$ne": None}}))
    if not docs:
        return None, 0.0

    embedding_list = []
    doc_list = []
    for doc in docs:
        emb_arr = np.array(doc["embedding_vector"], dtype=np.float32)
        embedding_list.append(emb_arr)
        doc_list.append(doc)

    embedding_matrix = np.stack(embedding_list, axis=0)
    new_emb = np.array(new_embedding, dtype=np.float32).reshape(1, -1)
    sim_scores = cosine_similarity(new_emb, embedding_matrix)[0]

    max_idx = np.argmax(sim_scores)
    max_sim = float(sim_scores[max_idx])
    best_doc = doc_list[max_idx]

    if max_sim >= threshold:
        return best_doc, max_sim
    else:
        return None, max_sim

def create_new_clothing(item_data):
    now = datetime.datetime.now(datetime.timezone.utc)
    item_data["created_at"] = now
    item_data["updated_at"] = now
    item_data["count"] = 1

    result = clothes_col.insert_one(item_data)
    return str(result.inserted_id)

def update_clothing_item(doc_id, item_data):
    existing = clothes_col.find_one({"_id": doc_id})
    if existing and "count" in existing:
        new_count = existing["count"] + 1
    else:
        new_count = 1

    item_data["count"] = new_count
    item_data["updated_at"] = datetime.datetime.now(datetime.timezone.utc)

    clothes_col.update_one({"_id": doc_id}, {"$set": item_data})
    return str(doc_id)

def read_clothing_item(doc_id: str):
    return clothes_col.find_one({"_id": ObjectId(doc_id)})

def delete_clothing_item(doc_id: str):
    result = clothes_col.delete_one({"_id": ObjectId(doc_id)})
    return result.deleted_count

def save_clothing_with_clip(image_url: str, extra_info: dict = None, threshold=0.9):
    if extra_info is None:
        extra_info = {}

    emb = get_clip_image_embedding(image_url)
    doc, sim = find_most_similar_embedding(emb, threshold=threshold)

    data_to_save = dict(extra_info)
    data_to_save["image_url"] = image_url
    data_to_save["embedding_vector"] = emb

    if doc:
        doc_id = doc["_id"]
        print(f"[동일 옷 판단] doc_id={doc_id}, sim={sim:.3f}")
        update_clothing_item(doc_id, data_to_save)
        return str(doc_id), "updated", sim
    else:
        print(f"[새 옷] max sim={sim:.3f} < threshold={threshold}")
        new_id = create_new_clothing(data_to_save)
        return new_id, "created", sim

#Demo
if __name__ == "__main__":
    test_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmMBPXvz72kW0mfNz6BgIFpOkudNPYpORcJQ&s"
    ai_metadata = {
        "category":"니트",
        "gender": "남",
        "season": "FW",
        "color": "블랙",
        "material": "울",
        "feature": "화란"
    }

    doc_id, action, sim = save_clothing_with_clip(test_image_url, ai_metadata, threshold=0.9)
    print(f"결과 => doc_id={doc_id}, action={action}, similarity={sim:.3f}")

    # 조회
    doc = read_clothing_item(doc_id)
    if doc:
        print("[문서 조회]", doc)
    else:
        print("[문서 조회] not found")
