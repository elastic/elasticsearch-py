FROM ubuntu:18.04
RUN apt-get update && apt-get install -y curl build-essential zlib1g-dev libssl1.0-dev
RUN ln -s /lib/i386-linux-gnu/libz.so.1 /lib/libz.so
RUN curl -s https://www.python.org/ftp/python/2.6.9/Python-2.6.9.tgz | tar -xzf -
WORKDIR Python-2.6.9
RUN LDFLAGS="-L/usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)" ./configure
RUN make
RUN make install
RUN curl https://bootstrap.pypa.io/2.6/get-pip.py -o get-pip.py
RUN python get-pip.py
