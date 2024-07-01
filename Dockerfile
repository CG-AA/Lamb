FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    make \
    g++ \
    libssl-dev \
    zlib1g-dev \
    libfmt-dev

# Wool dependencies
RUN apt-get install -y \
    libsodium-dev \
    libspdlog-dev

WORKDIR /app

RUN git clone --recurse-submodules https://github.com/uNetworking/uWebSockets && \
    cd uWebSockets && \
    make && \
    make install && \
    cd uSockets && \
    cp uSockets.a /usr/local/lib && \
    cp src/libusockets.h /usr/local/include

RUN git clone https://github.com/CG-AA/Wool && \
    cd Wool && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Lamb dependencies
RUN apt-get install -y \
    nlohmann-json3-dev

COPY . .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

CMD ["./Lamb"]