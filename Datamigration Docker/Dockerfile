FROM python:3

WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY migrate.py .

RUN mkdir /data /data/source /data/dest /data/logs /data/tmp

CMD [ "python", "./migrate.py" ]

# Docker command:
# Go to container location
# Copy the python script and dockerfile to the host that is used for the migration
# docker build . -t migrate:local
# docker run --name migratepy -d -v <source>:/data/source -v <dest>:/data/dest -v <logs>:/data/logs -v <tmp>:/data/tmp migrate:local