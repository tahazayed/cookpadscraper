FROM scrapinghub/base:14.04


WORKDIR /app
ADD requirements.txt /app/requirements.txt
ADD export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
RUN pip install pymssql
RUN pip install -r /app/requirements.txt
ADD . /app
