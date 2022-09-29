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
# docker run -v <src>:/data/source -v <dest>:/data/dest -v <logs>:/data/logs -v <tmp>/test/tmp:/data/tmp

# docker run --name migratepy -d -v /home/itsdone.local/robin.gjaltema/data/src:/data/source -v /home/itsdone.local/robin.gjaltema/data/dst:/data/dest -v /home/itsdone.local/robin.gjaltema/data/logs:/data/logs -v /home/itsdone.local/robin.gjaltema/data/tmp/:/data/tmp migrate:local
# docker container run -d -v /home/itsdone.local/robin.gjaltema/data/src:/data/source -v /home/itsdone.local/robin.gjaltema/data/dst:/data/dest -v /home/itsdone.local/robin.gjaltema/data/logs:/data/logs -v /home/itsdone.local/robin.gjaltema/data/tmp/test/tmp:/data/tmp migrate:local