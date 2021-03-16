FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/ErdemBey1/SiriUserBot /root/dtouserbot
WORKDIR /root/dtouserbot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"] 
