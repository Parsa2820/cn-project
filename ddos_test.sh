#!/bin/bash

ADDRESS="127.0.0.1"
PORT="2820"

for i in {0..12}
do
    echo "request $i"
    telnet $ADDRESS $PORT &
done