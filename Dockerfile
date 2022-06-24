FROM python:3.9-buster

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN ["rm /etc/apt/sources.list.d/*"]

cat <<EOF |sudo tee /etc/apt/sources.list
deb http://deb.debian.org/debian/ unstable main
EOF
# Install cmake
RUN apt-get update
RUN apt-get -y install cmake
RUN apt-get install libc6


RUN apt-get -y install --only-upgrade libc6

# # Install java
# RUN  apt-get update  -y \
#   && apt-get install -y software-properties-common \
#   && add-apt-repository ppa:openjdk-r/ppa \
#   && apt-get install -y -allow-unauthenticated openjdk-8-jdk \
#   && rm -rf /var/lib/apt/lists/*

COPY PyAlgorithms/requirements.txt PyAlgorithms/requirements.txt
RUN pip3 install -r PyAlgorithms/requirements.txt

COPY . .
RUN ["sh", "build_all.sh"]

# RUN ["cd", "PyAlgorithms/src"]
