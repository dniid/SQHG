#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

from fastapi import FastAPI

from core.database import BaseModel, engine

import admin.router
import sap.router
import survey.router
import user.router


BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(admin.router.router, prefix='/admin', tags=['Admin'])
app.include_router(sap.router.router, prefix='/sap', tags=['SAP'])
app.include_router(survey.router.router, prefix='/survey', tags=['Survey'])
app.include_router(user.router.router, prefix='/user', tags=['User'])
