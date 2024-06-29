FROM ubuntu:latses AS build

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++

WORKDIR /app
