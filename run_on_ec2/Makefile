SHELL:=/usr/bin/env bash

.PHONY: start
start:
	aws cloudformation create-stack --stack-name run-on-ec2 --template-body file://ec2_instance.yaml --region eu-central-1

.PHONY: info
info:
	aws cloudformation describe-stacks \
    --stack-name run-on-ec2 \
    --query 'Stacks[*].Outputs'

.PHONY: stop
stop:
	aws cloudformation delete-stack --stack-name run-on-ec2

.PHONY: logs
logs:
	$(eval INSTANCE_ID := $(shell aws cloudformation describe-stacks --stack-name run-on-ec2 --query 'Stacks[*].Outputs[?OutputKey==`InstanceId`].OutputValue' --output text))
	@echo INSTANCE_ID=$(INSTANCE_ID)
	aws ec2 get-console-output --instance-id $(INSTANCE_ID)  --output text

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
