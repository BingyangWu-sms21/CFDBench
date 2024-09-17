#!/bin/bash
if [ ! -d "data" ]; then
  mkdir data
fi
if [ ! -d "data/cylinder" ]; then
  mkdir data/cylinder
fi
unzip -qn -d data/cavity data_download/cavity.zip &
unzip -qn -d data/dam data_download/dam.zip &
unzip -qn -d data/tube data_download/tube.zip &
unzip -qn -d data/cylinder/bc data_download/cylinder/bc.zip &
unzip -qn -d data/cylinder/geo data_download/cylinder/geo.zip &
unzip -qn -d data/cylinder/prop data_download/cylinder/prop.zip &

wait
echo "All files have been unzipped"
