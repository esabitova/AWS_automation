BUCKET_NAME="bucketfortemplate"

execute: package build test main

package:
	aws cloudformation package --template .\cfn\template.yml --s3-bucket $(BUCKET_NAME) --output-template-file .\cfn\packaged-template.yml

build:
	python -m venv venv
	pip install -r requirements.txt -t venv/lib/site-packages

main:
	python main.py

test:
	python -m unittest tests/tests.py

