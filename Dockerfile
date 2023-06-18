FROM python:3.9

WORKDIR /pyristic_api
 
RUN mkdir tmp_files; touch api.log

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /pyristic_api/app

ENV PYTHONPATH=/pyristic_api/app:/pyristic_api/tmp_files

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
