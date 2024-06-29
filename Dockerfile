FROM ubuntu:latest AS build

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++ \
    nlohmann-json3-dev

WORKDIR /app/deps

RUN git clone https://github.com/yourWaifu/sleepy-discord.git && \
    cd sleepy-discord && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

WORKDIR /app

COPY . .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

CMD ["./build/Lamb"]