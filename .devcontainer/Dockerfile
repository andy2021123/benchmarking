FROM python:3.13-bookworm

RUN \
  pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir tqdm GitPython

RUN \
  apt update && \
  apt install -y git

COPY ./install/* ./install/

RUN \
  ./install/borg.sh && \
  ./install/duplicati.sh && \
  ./install/kopia.sh && \
  ./install/restic.sh
