FROM python:latest
LABEL Maintainer="anton.shepitko"
WORKDIR /usr/app/src
COPY main.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY . .
EXPOSE 8080

CMD ["python", "app/main.py"]