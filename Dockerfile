FROM python:3.9

WORKDIR '/app'

COPY '/requirements.txt' .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . . 

CMD ["python","manage.py", "runserver", "0.0.0.0:8090"]