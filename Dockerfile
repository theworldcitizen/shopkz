FROM python:3.9

RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src /usr/src/app/

EXPOSE 8000

CMD ["python", "/usr/src/app/main.py"]
VOLUME /demo