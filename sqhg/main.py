#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

from fastapi import FastAPI

from core.database import BaseModel, engine

import sap.router


BaseModel.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(sap.router.router, prefix='/sap', tags=['SAP'])
