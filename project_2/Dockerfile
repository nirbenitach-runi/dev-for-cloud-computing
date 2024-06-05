FROM hashicorp/terraform:1.0.0 AS terraform
FROM amazon/aws-cli:latest

RUN yum install -y jq zip vim python3 python3-pip
RUN pip3 install awscli --upgrade --user

WORKDIR /terraform
COPY --from=terraform /bin/terraform /bin/terraform

COPY . /terraform
WORKDIR /terraform

RUN pip3 install -r requirements.txt

RUN zip -r register_user.zip src/register_user.py /usr/lib/python3.*/site-packages/*
RUN zip -r send_message.zip src/send_message.py /usr/lib/python3.*/site-packages/*
RUN zip -r block_user.zip src/block_user.py /usr/lib/python3.*/site-packages/*
RUN zip -r create_group.zip src/create_group.py /usr/lib/python3.*/site-packages/*
RUN zip -r add_remove_users.zip src/add_remove_users.py /usr/lib/python3.*/site-packages/*
RUN zip -r send_group_message.zip src/send_group_message.py /usr/lib/python3.*/site-packages/*
RUN zip -r check_messages.zip src/check_messages.py /usr/lib/python3.*/site-packages/*

ENTRYPOINT [ "/bin/bash" ]