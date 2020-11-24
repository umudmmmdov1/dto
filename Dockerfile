# DTÖUserBot

FROM archlinux:latest
RUN git clone https://github.com/umudmmmdov1/DTOUserBot /root/DTOUserBot
WORKDIR /root/DTOUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
