#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1

cd src/app

uvicorn main:app --host 127.0.0.1 --port 8000