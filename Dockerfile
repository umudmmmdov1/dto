FROM sandy1709/catuserbot:latest

# Klonla
RUN git clone https://github.com/sandy1709/dtousetbot.git /root/dtouserbot
#working directory 
WORKDIR /root/dtouserbot

# Kitabxana
RUN pip3 install -U -r requirements.txt

ENV PATH="/root/dtouserbot/bin:$PATH"

CMD ["python3","-m","userbot"]
