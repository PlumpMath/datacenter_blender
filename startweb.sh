#!/bin/bash
nova boot --image ubuntu-14.04-amd64 --flavor r900.tiny --user-data cloudinit-webserver.txt --key-name lurh --security-group default,webserver --nic net-id=424277bf-f9f3-4ffa-a622-eaeb3a4206ae lurh9615-web
