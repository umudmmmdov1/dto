FROM archlinux:latest


RUN pacman -Syyu --noconfirm \
    aria2 \
    curl \
    chromium \
    ffmpeg \
    figlet \
    gcc \
    git \
    jq \
    libevent \
    libffi \
    libjpeg \
    libpng \
    libpqxx \
    libsystemd \
    libwebp \
    libxml2 \
    libxslt \
    linux-headers \
    musl \
    neofetch \
    nss \
    openssl \
    postgresql \
    postgresql-client \
    python3 \
    python-pip \
    pv \
    sudo \
    tzdata \
    util-linux \
    wget  


RUN git clone https://github.com/umudmmmdov1/DTOUserBot /root/dtouserbot
RUN mkdir /root/dtouserbot/bin/
WORKDIR /root/dtouserbot/


COPY ./sample_config.env ./userbot.session* ./config.env* /root/dtouserbot/


ENV TZ=Asia/Baku


RUN pip3 install -r requirements.txt


CMD ["python3","main.py"]
