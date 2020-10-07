FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p /opt/api
WORKDIR /opt/api

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY .env .
COPY api.py .
COPY mongo.py .
COPY templates/ templates/
COPY model/ model/
COPY route/ route/
EXPOSE 5000
ENTRYPOINT ["gunicorn" , "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "--threads=16", "--workers=4", "api:app"]