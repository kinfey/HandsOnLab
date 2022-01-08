
FROM nvcr.io/nvidia/l4t-tensorflow:r32.5.0-tf2.3-py3

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN pip3 install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple


RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-opencv 

RUN pip3 install flask pillow   -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY app /app
# Expose the port
EXPOSE 80
# Set the working directory
WORKDIR /app
# Run the flask server for the endpoints
CMD python3 -u app.py

##
# docker build . -t starwardemo
# docker run -p 127.0.0.1:80:80 -d starwardemo
# curl -X POST http://127.0.0.1/url -d '{ "url": "https://img1.baidu.com/it/u=3868911901,2977215387&fm=26&fmt=auto" }'