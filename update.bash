#!/bin/bash

#Script to zip and upload the source files

zip package.zip *.py
aws lambda update-function-code --function-name rosaryFunction --zip-file fileb://package.zip 
rm package.zip
