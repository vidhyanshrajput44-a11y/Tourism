from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import traceback
from gov_dashboard_data import get_heatmap_data, POLICY_LOG
from whatif_simulator import simulate_capacity_cap
from crowd_vision import estimate_crowd_from_image, list_sample_images, get_sample_image_bytes

gov_router = APIRouter(prefix="/gov", tags=["Government Dashboard"])

class WhatIfRequest(BaseModel):
    destination_id: str
    proposed_cap: int

@gov_router.get("/heatmap-data")
def api_get_heatmap():
    return get_heatmap_data()

@gov_router.post("/whatif")
def api_run_whatif(req: WhatIfRequest):
    result = simulate_capacity_cap(req.destination_id, req.proposed_cap)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@gov_router.get("/whatif/history")
def api_whatif_history():
    return POLICY_LOG

@gov_router.post("/crowd-vision/estimate")
async def api_estimate_crowd(
    destination_id: str = Form(...),
    sample_image_name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    try:
        if sample_image_name:
            image_bytes = get_sample_image_bytes(sample_image_name)
        elif file:
            image_bytes = await file.read()
        else:
            raise HTTPException(status_code=400, detail="Must provide sample_image_name or upload a file")
            
        result = estimate_crowd_from_image(image_bytes, destination_id)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@gov_router.get("/crowd-vision/samples")
def api_get_cv_samples():
    return list_sample_images()
