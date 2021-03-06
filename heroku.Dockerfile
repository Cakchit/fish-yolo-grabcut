FROM ubuntu:18.04
MAINTAINER Cuda Chen <clh960524@gmail.com>

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'
# install Python and Pip
#
# NOTE: libSM.so.6 is required for OpenCV Docker
# or you will get seg fault when import OpenCV
RUN apt-get update && \
    apt-get install -y \
    python3.7 python3-pip \
    libsm6 libxext6 libxrender-dev

# expose port 8501 for streamlit
EXPOSE 8501

# make app directiry
WORKDIR /streamlit-docker

# copy requirements.txt
COPY requirements.txt ./requirements.txt

# install dependencies
RUN pip3 install -r requirements.txt

# copy all files over
COPY . .

# set heroku_startup.sh to be executable
RUN chmod +x ./heroku_startup.sh

# download YOLO weights
RUN gdown --output ./yolo-fish/fish.weights --id 1L6JgzbFhC7Bb_5w_V-stAkPSgMplvsmq 

# launch streamlit app
ENTRYPOINT "./heroku_startup.sh" 
