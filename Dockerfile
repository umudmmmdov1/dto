# Docker
FROM alpine:edge

# Community repo
RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories

# Kitabxana

RUN apk add --no-cache=true --update \
    coreutils \
    bash \
    build-base \
    bzip2-dev \
    curl \
    figlet \
    gcc \
    g++ \
    git \
    sudo \
    util-linux \
    libevent \
    jpeg-dev \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl \
    neofetch \
    openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    openssl \
    pv \
    jq \
    wget \
    freetype \
    freetype-dev \
    python3 \
    python3-dev \
    readline-dev \
    sqlite \
    ffmpeg \
    w3m \
    libjpeg-turbo-dev \
    sqlite-dev \
    libc-dev \
    sudo \
    chromium \
    chromium-chromedriver \
    zlib-dev \
    jpeg 
    #

RUN curl https://cli-assets.heroku.com/install.sh

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# Reponu klonla

RUN git clone -b sql-extended https://github.com/umudmmmdov1/DTOUserBot /root/dtouserbot
RUN mkdir /root/dtouserbot/.bin
WORKDIR /root/dtouserbot/
ENV PATH="/root/dtouserbot/.bin:$PATH"
WORKDIR /root/dtouserbot/
#
# Copies session and config (if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /root/dtouserbot/

# Yüklenme requirements
RUN pip3 install -r requirements.txt
CMD ["python3","main.py"]
