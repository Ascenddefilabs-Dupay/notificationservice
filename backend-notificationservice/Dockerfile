FROM python:3.11-slim

WORKDIR /backend-notification

COPY requirements.txt /backend-notificationservice/
RUN pip3 install -r /backend-notificationservice/requirements.txt


COPY . .
# RUN python main_consumer.py


CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]

# CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8003 & python main_consumer.py"]
