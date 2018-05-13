FROM scrapinghub/base:14.04


WORKDIR /app
ADD export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
