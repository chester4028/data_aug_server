FROM python:3.7-slim

# install node env for pyexecjs
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y xz-utils 
RUN wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz 
RUN xz -d node-v10.15.3-linux-x64.tar.xz
RUN tar -xvf node-v10.15.3-linux-x64.tar

# 添加软链接
RUN ln -s /node-v10.15.3-linux-x64/bin/node /usr/local/bin/node 

COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["sh","./gunicorn_starter.sh"]
