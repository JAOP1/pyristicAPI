FROM python:3.9

WORKDIR /pyristic_api
 
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /pyristic_api/app

RUN mkdir app/optimization_problem && touch app/optimization_problem/__init__.py

ENV PYTHONPATH=/pyristic_api/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
