FROM python:3.10

# Set the working directory to /app
WORKDIR /usr/src/app

# Install any required Python packages
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

ADD . .


ENTRYPOINT ["/bin/sh", "-c" , "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn -b 0.0.0.0:8000 AccuracyTestBackend.wsgi"]
