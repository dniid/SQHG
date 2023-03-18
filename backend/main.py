#!/usr/bin/env python3
"""Main FastAPI app for SQHG's backend."""

from fastapi import FastAPI

# import module.router


app = FastAPI()


@app.get('/')
async def hello():
    return "Hello!"

# app.include_router(modules.router.router, prefix='/modules', tags=['Modules'])
