SHELL:=/usr/bin/env bash

$(V).SILENT:

.PHONY: .env
.env: .env.op
	op inject -f -i .env.op -o .env

userdata.sh: .env userdata_template.sh
	set -a && source .env && set +a && envsubst < userdata_template.sh > userdata.sh


.PHONY: all
all: start logs

.PHONY: start
start: userdata.sh
	# aws cloudformation create-stack --stack-name run-on-ec2 --template-body file://ec2_instance.yaml
	aws cloudformation create-stack --stack-name run-on-ec2 --template-body file://ec2_instance.yaml --parameters ParameterKey=UserDataFile,ParameterValue=$(shell  base64  -b -i userdata.sh)
	aws cloudformation wait stack-create-complete --stack-name run-on-ec2
	# rm userdata.sh

.PHONY: info
info:
	aws cloudformation describe-stacks \
    --stack-name run-on-ec2 \
    --query 'Stacks[*].Outputs'

.PHONY: stop
stop:
	aws cloudformation delete-stack --stack-name run-on-ec2
	aws cloudformation wait stack-delete-complete --stack-name run-on-ec2

.PHONY: logs_
logs_:
	$(eval INSTANCE_ID := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text))
	@echo INSTANCE_ID=$(INSTANCE_ID)
	aws ec2 get-console-output --instance-id $(INSTANCE_ID)  --output text

.PHONY: my_key
my_key:
	$(eval INSTANCE_ID := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text))
	@echo INSTANCE_ID=$(INSTANCE_ID)
	ssh-keygen -t rsa -f my_key -N '' <<<y
	aws ec2-instance-connect send-ssh-public-key  --instance-id $(INSTANCE_ID)  --instance-os-user ubuntu  --ssh-public-key file://my_key.pub


.PHONY: logs
logs: my_key
	$(eval PUBLIC_IP := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`PublicIP`].OutputValue' --output text))
	ssh -o "IdentitiesOnly=yes"  -o "StrictHostKeyChecking no" -i my_key ubuntu@$(PUBLIC_IP)  'tail -c +0 -f /var/log/cloud-init-output.log'

.PHONY: ssh
ssh:
	$(eval INSTANCE_ID := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text))
	$(eval PUBLIC_IP := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`PublicIP`].OutputValue' --output text))
	@echo INSTANCE_ID=$(INSTANCE_ID)
	ssh-keygen -t rsa -f my_key -N '' <<<y
	aws ec2-instance-connect send-ssh-public-key \
    --instance-id $(INSTANCE_ID) \
    --instance-os-user ubuntu \
    --ssh-public-key file://my_key.pub
	ssh -o "IdentitiesOnly=yes"  -o "StrictHostKeyChecking no" -i my_key ubuntu@$(PUBLIC_IP)

.PHONY: browser
browser:
	$(eval INSTANCE_ID := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text))
	@echo INSTANCE_ID=$(INSTANCE_ID)
	open https://eu-central-1.console.aws.amazon.com/ec2-instance-connect/ssh\?connType\=standard\&instanceId\=$(INSTANCE_ID)\&osUser\=ubuntu\&region\=eu-central-1\&sshPort\=22\#

.PHONY: docker
docker:
	docker run \
    --log-driver=awslogs \
    --log-opt awslogs-create-group=true \
    --log-opt awslogs-region=eu-central-1 \
    --log-opt awslogs-group=myLogGroup \
    -it ubuntu bash -c 'for i in {0..10000}; do echo $i; sleep 1; done'

#     --log-opt awslogs-datetime-format='\[%b %d, %Y %H:%M:%S\]' \
