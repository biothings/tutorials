FROM praqma/network-multitool:latest
LABEL "path"="/tmp/annotations.zip"
LABEL "dump_command"="/usr/bin/wget https://s3.pgkb.org/data/annotations.zip -O /tmp/annotations.zip"
LABEL keep_container="true"
LABEL container_name=tutorials
