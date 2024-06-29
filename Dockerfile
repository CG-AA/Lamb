FROM ubuntu:latses AS build

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++

WORKDIR /building

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

FROM ubuntu:latest AS runtime

WORKDIR /app

COPY --from=build /app/build/bot .