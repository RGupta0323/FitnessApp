# syntax=docker/dockerfile:1

FROM python

WORKDIR /FitnessApp/

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY src/ .

CMD [ "python", "./src/FlaskWebApp/app.py"]