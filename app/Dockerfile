FROM tiangolo/uvicorn-gunicorn:python3.8
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
ENV PYTHONUNBUFFERED=0

EXPOSE 80
