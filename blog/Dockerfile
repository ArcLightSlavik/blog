FROM python:3.7.7-slim

COPY techy/requirements.txt .
RUN pip install -r requirements.txt

ADD . /techy
WORKDIR /techy

ENV PORT 8000
CMD ["gunicorn", "-b", ":8000", "-k", "uvicorn.workers.UvicornWorker", "--reload", "techy.main:app"]
