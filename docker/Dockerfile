FROM python:3.11-slim

LABEL org.opencontainers.image.title="ai-mindmap-wizard"
LABEL org.opencontainers.image.description="AI思维可视化引擎 — 一键部署全管道"

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-tra \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY tools/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install python-pptx pytest requests beautifulsoup4

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "tools/pipeline.py"]
CMD ["--help"]
