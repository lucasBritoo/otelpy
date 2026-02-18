from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter
from otelpy import set_span_attribute, TraceInstruments
import asyncio

import os

router = APIRouter(
    prefix=f"{os.environ['SERVICE_ROOT_PATH']}/stress",
    tags=['stress']
)

@router.get("/stress_01")
async def get_stress_01():
    await asyncio.sleep(5)
    return {"status": "done"}