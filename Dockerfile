FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=godsings
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
