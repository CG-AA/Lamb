FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    libssl-dev \
    libcurl4-openssl-dev \
    g++ \
    nlohmann-json3-dev

WORKDIR /app

COPY . .

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make

CMD ["./build/Lamb"]