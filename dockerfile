FROM python:3.9
WORKDIR /app
RUN git clone -b prod https://github.com/adampalmergithub/addressBook.git
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=myproject.settings
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it
COPY create_superuser.py /app/create_superuser.py
RUN chmod 777 create_superuser.py
COPY . /app/
CMD /usr/local/bin/wait-for-it mysql-db:3306 -- && \ 
    cd /app/addressBook/myproject && \
    python manage.py makemigrations && \
    echo "Running migrations..." && python manage.py migrate && \
    echo "Creating superuser..." && python manage.py shell < /app/create_superuser.py && \
    echo "Starting server..." && python manage.py runserver 0.0.0.0:80
