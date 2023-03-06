FROM python:3.9

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing scipy
RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.7.1

# Installing other packages
RUN pip3 install --no-cache-dir \
    pandas==1.3.5 \
    numpy==1.21.4 \
    psycopg2-binary==2.9.1 \
    scikit-learn==1.0.2 \
    matplotlib==3.5.1 \
    scikit-optimize==0.9.0

COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app

COPY ./entrypoint.sh /usr/src/app
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
