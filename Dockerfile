FROM gengkapak/archlinux:latest
USER gengkapak


RUN git clone -b master https://github.com/umudmmmdov1/DTOUserBot /root/dtouserbot
RUN mkdir /root/dtouserbot/bin/
WORKDIR /root/dtouserbot/

CMD ["python3", "main.py"]
