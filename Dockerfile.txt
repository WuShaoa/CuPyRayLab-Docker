# syntax=docker/dockerfile:1
FROM nvidia/cuda:12.3.1-devel-ubuntu22.04

# install app dependencies
RUN sed -i "s@http://archive.ubuntu.com@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install --no-install-recommends libffi-dev python3 python3-pip liblzma-dev apt-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple/ \
    && pip3 config set global.trusted-host mirrors.aliyun.com \
    && pip3 install --upgrade pip \
    && pip3 install -r /requirements.txt \
    && pip3 cache purge
# generate jupyter config
RUN jupyter-lab --generate-config
    # && echo "c.NotebookApp.password = u'666666'" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.port = 8080" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.allow_origin = '*'" >> /root/.jupyter/jupyter_notebook_config.py \
    # && echo "c.NotebookApp.allow_remote_access = True" >> /root/.jupyter/jupyter_notebook_config.py

# final configuration
EXPOSE 6379 8080 8888 8265

RUN mkdir /hf_cache \
    && chmod -R 777 /hf_cache
RUN mkdir /workspace \
    && chmod -R 777 /workspace
ENV PATH="/root/.local/bin:${PATH}"
ENV TRANSFORMERS_CACHE="/hf_cache"
ENV RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER="1"

VOLUME [ "/hf_cache", "/workspace"]

CMD echo "-----successful------" \ 
    && ray start --head --port=6379 --dashboard-host='0.0.0.0' \
    && bin/sh

# docker build -f .\Dockerfile.txt -t pyraylab:v0.1 . 
# docker run -it  --shm-size=1.10gb -p 6379:6379 -p 8265:8265 -p 8080:8080 -p 8888:8888 -v D:\dev\raydocker\workspace:/workspace -v D:\dev\raydocker\hf_cache:/hf_cache pyraylab:v0.12 /bin/bash
# jupyter-lab password && jupyter-lab --allow-root --ip 0.0.0.0 --port 8080 --no-browser