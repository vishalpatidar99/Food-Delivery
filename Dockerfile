FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
COPY . /app
EXPOSE 9998
RUN python -m pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:9998" ]
