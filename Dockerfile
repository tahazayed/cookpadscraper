FROM scrapinghub/base:14.04

RUN apt-get update && apt-get install -y \
    freetds-bin \
    freetds-common \
    freetds-dev
	
RUN pip install Cython
RUN pip install ipython
RUN pip install SQLAlchemy
RUN pip install pandas
RUN pip install Alembic

# Add source directory to Docker image
# Note that it's beneficial to put this as far down in the Dockerfile as
# possible to maximize the chances of being able to use image caching
ADD . /opt/src/pymssql/

RUN pip install /opt/src/pymssql

WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
