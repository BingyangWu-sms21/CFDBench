#!/bin/bash
if [ ! -d "log" ]; then
    mkdir log
fi
if [ ! -d "log/download" ]; then
    mkdir log/download
fi
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/cavity.zip -c -P data_download -o log/download/cavity.log &
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/dam.zip -c -P data_download -o log/download/dam.log &
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/tube.zip -c -P data_download -o log/download/tube.log &
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/cylinder/bc.zip -c -P data_download/cylinder -o log/download/cylinder_bc.log &
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/cylinder/geo.zip -c -P data_download/cylinder -o log/download/cylinder_geo.log &
wget https://hf-mirror.com/datasets/chen-yingfa/CFDBench/resolve/main/cylinder/prop.zip -c -P data_download/cylinder -o log/download/cylinder_prop.log &

wait
echo "All files have been downloaded"
