FROM python:3.6

ENV ROOT_DIR /usr/src
ENV PYTHONUNBUFFERED=1

# WRK (HTTP benchmarking tool)
RUN git clone https://github.com/wg/wrk.git /tmp/wrk
WORKDIR /tmp/wrk
RUN make
RUN cp /tmp/wrk/wrk /usr/local/bin

WORKDIR ${ROOT_DIR}
RUN pip install -U pip
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . ${ROOT_DIR}

CMD ["python", "run.py"]
