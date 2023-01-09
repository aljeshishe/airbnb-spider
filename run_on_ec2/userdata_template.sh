#!/bin/bash
set -ex

echo "preparing environment"
sudo apt update -y
sudo apt install -y docker.io mc awscli  curl
# for debug
sudo apt install -y mc
aws --profile default configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
aws --profile default configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
aws --profile default configure set region eu-central-1
# sudo service docker start

echo "running docker"
sudo docker run -t ubuntu bash -c 'for i in {0..10}; do echo $i; sleep 1; done'


echo "stopping instance"
aws cloudformation delete-stack --stack-name run-on-ec2
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" -d chat_id=99044115 -d text="job done"
