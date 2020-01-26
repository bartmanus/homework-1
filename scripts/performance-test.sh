#! /usr/bin/env bash
export endpoints=http://10.20.30.40/{,dynamic}

podman pull docker.io/williamyeh/wrk:latest

for url in $endpoints
do
    podman run --rm docker.io/williamyeh/wrk:latest -c 400 -d 60 --latency $url
done

