FROM python:slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

ENV DJANGO_DEBUG_FALSE=1

# Read Railway environment variables
ARG DJANGO_SECRET_KEY
ARG DJANGO_ALLOWED_HOST

RUN python manage.py collectstatic
RUN python manage.py migrate --noinput

CMD ["gunicorn", "superlists.wsgi:application"]