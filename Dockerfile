FROM hashicorp/terraform:1.0.0 AS terraform
FROM amazon/aws-cli:latest

RUN yum install -y jq zip vim python3 python3-pip
RUN pip3 install awscli --upgrade --user

WORKDIR /terraform
COPY --from=terraform /bin/terraform /bin/terraform

COPY . /terraform
WORKDIR /terraform

RUN pip3 install -r requirements.txt
RUN zip -r entry_lambda.zip entry_lambda.py /usr/lib/python3.*/site-packages/*
RUN zip -r exit_lambda.zip exit_lambda.py /usr/lib/python3.*/site-packages/*

ENTRYPOINT [ "/bin/bash" ]