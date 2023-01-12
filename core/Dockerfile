# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/src/citationweb

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install \
    netcat \
    postgresql \
    postgresql-client \
    postgresql-contrib \
    libxml2-dev \
    libxslt-dev \
    gfortran \
    -y

# install dependencies
RUN pip install --upgrade pip
RUN pip install pip-conflict-checker
RUN pipconflictchecker
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/citationweb/entrypoint.sh
#RUN chmod +x /usr/src/citationweb/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
# ENTRYPOINT ["/usr/src/citationweb/entrypoint.sh"]
CMD ["uvicorn", "routes:app", "--host", "0.0.0.0", "--port", "80"]
