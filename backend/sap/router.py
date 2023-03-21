"""SAP's FastAPI router endpoints for SQHG's backend."""

from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import Database

from sap.models import (
    Superior,
    Area
)
from sap.schemas import (
    AreaSchema,
    AreaCreate,
    AreaUpdate,
    Superior,
    SuperiorCreate
)


router = APIRouter()


@router.post("/area/", response_model=AreaSchema)
async def create_area(area: AreaCreate, db: Session = Depends(Database)):
    db_area = Area(**area.dict())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area


@router.get("/area/", response_model=List[AreaSchema])
async def read_areas(skip: int = 0, limit: int = 100, db: Session = Depends(Database)):
    areas = db.query(Area).offset(skip).limit(limit).all()
    return areas


@router.get("/area/{area_id}/", response_model=AreaSchema)
async def detail_area(area_id: int, db: Session = Depends(Database)):
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    return db_area


@router.put("/area/{area_id}/")
async def update_area(area_id: int, area: AreaUpdate, db: Session = Depends(Database)):
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    for key, value in area.dict(exclude_unset=True).items():
        setattr(db_area, key, value)
    db.commit()
    db.refresh(db_area)
    return db_area


@router.delete("/area/{area_id}/")
async def delete_area(area_id: int, db: Session = Depends(Database)):
    db_area = db.query(Area).filter(Area.id == area_id).first()
    if not db_area:
        raise HTTPException(status_code=404, detail="Area not found")
    db.delete(db_area)
    db.commit()
    return {"message": "Area deleted"}
