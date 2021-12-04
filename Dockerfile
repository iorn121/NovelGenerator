# FROM python:3
# USER root

# RUN apt-get update
# RUN apt-get -y install locales && \
#     localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
# ENV LANG ja_JP.UTF-8
# ENV LANGUAGE ja_JP:ja
# ENV LC_ALL ja_JP.UTF-8
# ENV TZ JST-9
# ENV TERM xterm

# RUN mkdir -p /root/src
# RUN mkdir -p /root/data
# RUN mkdir -p /root/output
# COPY requirements.txt /root/src
# COPY data/ /root/data
# WORKDIR /root/src

# RUN pip install --upgrade pip
# RUN pip install --upgrade setuptools
# RUN pip install -r requirements.txt

########## Pull ##########
FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04
########## BASIS ##########
RUN apt-get update && apt-get install -y \
    vim \
    wget \
    unzip \
    git \
    build-essential
########## PyTorch ##########
RUN apt-get update && \
    apt-get install -y \
    python3-pip && \
    pip3 install --upgrade "pip < 21.0" && \
    pip3 install \
    torch==1.0.0 \
    torchvision==0.2.1
########## Book "pytorch_advanced" ##########
RUN cd /home && \
    git clone https://github.com/YutaroOgawa/pytorch_advanced
########## Jupyter Notebook ##########
RUN pip3 install jupyter && \
    echo "#!/bin/bash \n \
    cd /home/pytorch_advanced && \n \ 
    jupyter notebook --port 8000 --ip=0.0.0.0 --allow-root" \
    >> /home/jupyter_notebook.sh && \
    chmod +x /home/jupyter_notebook.sh
########## Requirements ##########
RUN apt-get update && \
    apt-get install -y \
    libopencv-dev && \
    pip3 install \
    matplotlib \
    tqdm \
    opencv-python \
    pandas
######### Initial position ##########
WORKDIR /home