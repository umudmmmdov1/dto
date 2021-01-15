FROM sandy1709/catuserbot:latest

#clonning repo 
RUN git clone https://github.com/umudmmmdov1/dtouserbot.git /root/dtouserbot
#working directory 
WORKDIR /root/dtouserbot

# Install requirements
RUN pip3 install -U -r requirements.txt

ENV PATH="/home/dtouserbot/bin:$PATH"

CMD ["python3", "main.py"]
