# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /FitnessApp/

COPY /FitnessApp .



COPY src/FlaskWebApp .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]