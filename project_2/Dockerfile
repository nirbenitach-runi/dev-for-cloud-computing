FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
        wget \ 
        jq \
        zip \
        vim \
        curl \
        python3 \
        python3-pip \
        unzip && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip && \
    unzip terraform_1.0.0_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.0.0_linux_amd64.zip

RUN pip3 install awscli --upgrade --user
RUN pip3 install pytest requests

WORKDIR /terraform
COPY . /terraform
COPY src/ .

RUN pip3 install -r /terraform/requirements.txt

RUN cd /terraform && \
    zip -r register_user.zip register_user.py /usr/lib/python3.*/site-packages/* && \
    zip -r send_message.zip send_message.py /usr/lib/python3.*/site-packages/* && \
    zip -r block_user.zip block_user.py /usr/lib/python3.*/site-packages/* && \
    zip -r create_group.zip create_group.py /usr/lib/python3.*/site-packages/* && \
    zip -r add_remove_users.zip add_remove_users.py /usr/lib/python3.*/site-packages/* && \
    zip -r send_group_message.zip send_group_message.py /usr/lib/python3.*/site-packages/* && \
    zip -r check_messages.zip check_messages.py /usr/lib/python3.*/site-packages/*

RUN rm -r src *.py

ENTRYPOINT [ "/bin/bash" ]