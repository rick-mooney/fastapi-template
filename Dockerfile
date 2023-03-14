FROM python:3.10.8

EXPOSE 80
EXPOSE 8000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]