FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++ \
    nlohmann-json3-dev \
    zlib1g-dev \
    libsodium-dev \
    libspdlog-dev

WORKDIR /app

# install uWebSockets
RUN git clone --recurse-submodules https://github.com/uNetworking/uWebSockets.git && \
    cd uWebSockets && \
    WITH_OPENSSL=1 make && \
    make install && \
    cp -r ./uSockets/uSockets.a /usr/lib/ && \
    mkdir /usr/include/uSockets && \
    cp -r ./uSockets/src/* /usr/include/uSockets/

# break the cache
ARG CACHEBUSTER=1

RUN git clone https://github.com/CG-AA/Wool && \
    cd Wool && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

COPY . .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

CMD ["./build/Lamb"]