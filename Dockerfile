FROM scrapinghub/base:12.04
ENV PYTHON_VERSION python-3.6.1
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
