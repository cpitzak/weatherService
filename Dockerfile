FROM hypriot/rpi-python:2.7

# Create app directory
RUN mkdir -p /apps/weatherService
WORKDIR /apps/weatherService

# Install dependencies
RUN pip install pymongo==3.2.2

COPY . /apps/weatherService

CMD [ "python", "job.py" ]