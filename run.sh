#!/bin/bash

# x=`lsof -Fp -i:4000`
# kill -9 ${x##p}
# x=`lsof -Fp -i:4001`
# kill -9 ${x##p}
# x=`lsof -Fp -i:4002`
# kill -9 ${x##p}
# x=`lsof -Fp -i:4003`
# kill -9 ${x##p}

input="processes.txt"
while IFS= read -r line
do
  echo "killing $line"
  kill "$line"
done < "$input"

rm "processes.txt"

python3 cache_server.py 0 &
python3 cache_server.py 1 &
python3 cache_server.py 2 &
python3 cache_server.py 3 &
python3 cache_client_chs.py 

# start cmd.exe /k "cd Desktop\cmpe273\cmpe273-assignment3 && python3 cache_server.py 2"