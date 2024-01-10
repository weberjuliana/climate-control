FROM python:3.8

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install debugpy

COPY . .

CMD ["uvicorn", "climatecontrol.src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
