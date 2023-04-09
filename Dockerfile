from python:3.10

RUN mkdir -p /home/app/webapp

WORKDIR /home/app/webapp

RUN pip install --upgrade pip  

COPY . /home/app/webapp

RUN pip install -r requirements.txt