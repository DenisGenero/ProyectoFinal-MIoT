#!/bin/bash
cd backend
source ./venv/Scripts/activate
sleep 1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload