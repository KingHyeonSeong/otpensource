# main.py
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional
from db_ops import (
    save_clothing_with_clip,
    read_clothing_item,
    delete_clothing_item
)

app = FastAPI()

class ClothingInfo(BaseModel):
    category: Optional[str] = Field("", description="카테고리")
    gender: Optional[str] = Field("", description="성별")
    season: Optional[str] = Field("", description="시즌")
    color: Optional[str] = Field("", description="색상")
    material: Optional[str] = Field("", description="재질")
    feature: Optional[str] = Field("", description="특징")

@app.post("/upload")
def upload_clothing(image_url: str, info: ClothingInfo, threshold: float = 0.90):
    """
    클라이언트가 image_url + 기타정보를 보내면
    CLIP 임베딩 -> DB에 저장 or 업데이트
    """
    doc_id, action, sim = save_clothing_with_clip(
        image_url=image_url,
        extra_info=info.model_dump(),
        threshold=threshold
    )
    return {"doc_id": doc_id, "action": action, "similarity": sim}

@app.get("/clothes/{doc_id}")
def get_clothes(doc_id: str):
    doc = read_clothing_item(doc_id)
    if doc:
        doc["_id"] = str(doc["_id"]) 
        return doc
    else:
        return {"message": "not found"}

@app.delete("/clothes/{doc_id}")
def remove_clothes(doc_id: str):
    deleted = delete_clothing_item(doc_id)
    return {"deleted_count": deleted}
