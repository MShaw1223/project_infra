FROM python:3.9
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=myproject.settings
COPY create_superuser.py /app/
WORKDIR /app
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it
COPY create_superuser.py /app/create_superuser.py
COPY . .
CMD /usr/local/bin/wait-for-it mysql-db:3306 -- python manage.py migrate && \
    python manage.py shell < /app/create_superuser.py && \
    python manage.py runserver 0.0.0.0:80
