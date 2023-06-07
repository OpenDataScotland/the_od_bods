FROM python:3.9-buster

WORKDIR /usr/src/app

COPY . the_od_bods

RUN mkdir -p jkan/_datasets

WORKDIR /usr/src/app/the_od_bods

RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh run.sh

RUN chmod a+x run.sh

CMD ["./run.sh"]