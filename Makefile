VERSION=$(shell git rev-parse --short HEAD)
DESC=$(shell git log -1 --pretty=%B)
BUCKET_NAME="my-bucket"
PROJECT_NAME="AWS_automation"
REGION="eu-west-2"
ENV_NAME="elasticbeanstalk-environment-name"

## Only run install if requirements.txt is newer than SITE_PACKAGES location
#.PHONY: install
#SITE_PACKAGES := $(shell pip show pip | grep '^Location' | cut -f2 -d':')
#install: $(SITE_PACKAGES)
#
#$(SITE_PACKAGES): requirements.txt
#    pip install -r requirements.txt
#
#.PHONY: virtual install build-requirements black isort flake8
#
#virtual: .venv/bin/pip # Creates an isolated python 3 environment
#
#.venv/bin/pip:
#	virtualenv -p /usr/bin/python3 .venv
#
#install:
#	.venv/bin/pip install -Ur requirements.txt


package_command:
	#aws cloudformation package --template cfn/template.yml --s3-bucket $(BUCKET_NAME) --output yml > packaged-template.yml
	aws cloudformation package --template .\cfn\template.yml --s3-bucket bucketfortemplate --output-template-file packaged-template.yml



deploy: install_environment package_command