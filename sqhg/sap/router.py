"""SAP's FastAPI router endpoints for SQHG's backend."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import Database

from sap.models import (
    Area
)
from sap.schemas import (
    AreaSchema,
    AreaCreate,
    AreaUpdate
)


router = APIRouter()


@router.post('/create', response_model=AreaSchema)
async def create_area(area: AreaCreate, database: Session = Depends(Database)):
    database_area = Area(**area.dict())
    database.add(database_area)
    database.commit()
    database.refresh(database_area)
    return database_area


@router.get('/', response_model=List[AreaSchema])
async def read_areas(skip: int = 0, limit: int = 100, database: Session = Depends(Database)):
    return database.query(Area).offset(skip).limit(limit).all()


@router.get('/{area_id}/', response_model=AreaSchema)
async def detail_area(area_id: int, database: Session = Depends(Database)):
    database_area = database.query(Area).filter(Area.id == area_id).first()
    if not database_area:
        raise HTTPException(status_code=404, detail='Area not found')
    return database_area


@router.put('/{area_id}/', response_model=AreaSchema)
async def update_area(area_id: int, area: AreaUpdate, database: Session = Depends(Database)):
    database_area = database.query(Area).filter(Area.id == area_id).first()
    if not database_area:
        raise HTTPException(status_code=404, detail='Area not found')
    for key, value in area.dict(exclude_unset=True).items():
        setattr(database_area, key, value)
    database.commit()
    database.refresh(database_area)
    return database_area


@router.delete('/{area_id}/')
async def delete_area(area_id: int, database: Session = Depends(Database)):
    database_area = database.query(Area).filter(Area.id == area_id).first()
    if not database_area:
        raise HTTPException(status_code=404, detail='Area not found')
    database.delete(database_area)
    database.commit()
    return {'message': 'Area deleted'}
