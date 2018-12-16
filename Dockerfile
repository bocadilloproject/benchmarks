FROM python:3.6

ENV ROOT_DIR /usr/src

WORKDIR ${ROOT_DIR}
RUN pip install -U pip
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . ${ROOT_DIR}

CMD ["python", "run.py"]
