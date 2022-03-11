FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y \
    apache2 \
    apache2-dev \
    apache2-utils \
    libexpat1 \
    ssl-cert \
    python3\
    libapache2-mod-wsgi \
    sudo \
    python3-pip \
    virtualenv \
    wget \
    python3-venv \
    git

COPY requirements.txt requirements.txt
RUN pip3 install -r /requirements.txt
# hack to make python3 version of geoip working
RUN pip3 uninstall --yes python-geoip
RUN pip3 install  python-geoip-python3==1.3
ENTRYPOINT ["/topcons/dockerrun.sh"]
