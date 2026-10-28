FROM python:3.11-slim


WORKDIR /app

#install Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --default-timeout=120 \
    --retries=10 \
    -r requirements.txt

# Copy backend code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV CHROMA_PERSIST_DIRECTORY=/app/data/chroma
ENV UPLOAD_DIR=/app/uploads
ENV TESSERACT_CMD=/usr/bin/tesseract

RUN mkdir -p /app/data/chroma /app/uploads

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]