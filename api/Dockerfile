FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python /app/setup.py install && python /app/setup.py develop
EXPOSE 6540
CMD [ "uwsgi", "--ini-paste", "production.ini" ]
