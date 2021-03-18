FROM sandy1709/catuserbot:latest
RUN git clone https://github.com/umudmmmdov1/dtouserbot.git /root/dtouserbot
WORKDIR /root/dtouserbot
RUN pip3 install -U -r requirements.txt
ENV PATH="/home/dtouserbot/bin:$PATH"
CMD ["python3", "main.py"]
