FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++ \
    nlohmann-json3-dev \
    zlib1g-dev

WORKDIR /app

# install uWebSockets
RUN git clone --recurse-submodules git@github.com:uNetworking/uWebSockets.git && \
    cd uWebSockets && \
    WITH_OPENSSL=1 make && \
    make install

RUN git clone https://github.com/CG-AA/Wool

COPY . .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

CMD ["./build/Lamb"]