# AI App Generator

This project converts natural language into structured application configurations using a multi-stage pipeline.

## Pipeline
1. Intent Extraction
2. System Design
3. Schema Generation
4. Validation
5. Retry Mechanism

## Features
- Structured JSON output
- Validation system
- Retry logic for reliability
- Simple UI demo

## Run locally
py -m uvicorn app:app --reload

Open:
http://127.0.0.1:8000/ui
