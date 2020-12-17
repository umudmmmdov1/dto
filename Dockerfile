FROM gengkapak/archlinux:latest
USER gengkapak


RUN git clone -b master https://github.com/umudmmmdov1/DTOUserBot /home/dtouserbot
RUN mkdir /home/dtouserbot/bin/
WORKDIR /home/dtouserbot/

CMD ["python3", "main.py"]
