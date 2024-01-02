FROM python:3.11-slim

WORKDIR /home/strava/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

WORKDIR /home/strava/scrava/cli

CMD ["bash"]

