#!/bin/bash
vars=("u" "v")
axis=0
duration=0.1
max_frames=40
types=("bc" "prop" "geo")
log_dir=log/visual
temp_dir=tmp

if [ -d $temp_dir ]; then
    rm -r $temp_dir
fi

# cavity
python utils/visual.py --name cavity --dir data/cavity --out_dir gif --log_dir $log_dir --vars ${vars[@]} --types ${types[@]} --cases_start 0 50 1 --cases_end 50 134 25 --axis $axis --duration $duration --max_frames $max_frames &

# cylinder
python utils/visual.py --name cylinder --dir data/cylinder --out_dir gif --log_dir $log_dir --vars ${vars[@]} --types ${types[@]} --cases_start 0 50 1 --cases_end 50 166 21 --axis $axis --duration $duration --max_frames $max_frames &

# dam
python utils/visual.py --name dam --dir data/dam --out_dir gif --log_dir $log_dir --vars ${vars[@]} --types ${types[@]} --cases_start 0 70 170 --cases_end 70 170 220 --axis $axis --duration $duration --max_frames $max_frames &

# tube
python utils/visual.py --name tube --dir data/tube --out_dir gif --log_dir $log_dir --vars ${vars[@]} --types ${types[@]} --cases_start 0 50 150 --cases_end 50 150 175 --axis $axis --duration $duration --max_frames $max_frames &

wait
echo "All GIF files have been created successfully"
