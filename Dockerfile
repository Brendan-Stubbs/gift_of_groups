FROM python:3.9

ENV PYTHONBUFFERED 1
WORKDIR '/app'

COPY '/requirements.txt' .
RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8090


# Creates virtual environment, updates pips, install dependencies
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

COPY . . 

ENV PATH="/py/bin:$PATH"

USER django-user

# CMD ["python","manage.py", "runserver", "0.0.0.0:8090"]