"""User's FastAPI router endpoints for SQHG's backend."""

from fastapi import APIRouter


router = APIRouter()


@router.get('/')
async def dummy_endpoint():
    return {'message': 'user'}
