from pydantic import BaseModel, Field

class SlicerConfigV1(BaseModel):
    material: str = Field(...)
    nozzle_mm: float = Field(..., ge=0.1, le=2.0)
    layer_height_mm: float = Field(..., ge=0.05, le=0.6)
    print_speed_mm_s: int = Field(..., ge=5, le=300)
    infill_percent: int = Field(..., ge=0, le=100)
    supports: bool
    bed_temp_c: int = Field(..., ge=0, le=130)
    nozzle_temp_c: int = Field(..., ge=0, le=320)
    notes: str = ""
