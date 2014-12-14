#!/bin/bash

curl -i -X POST -F file=@$1 128.138.202.13:8080/upload
