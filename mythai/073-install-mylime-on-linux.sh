#!/usr/bin/env bash


set -e
set -x
set -u



timeout 1m bash -c '
  echo waiting for network
  until ping -c 1 google.com &>/dev/null
  do
    sleep 1
  done
'



if [[ -d /opt/ringgem ]]; then
    cd /opt/ringgem
    git fetch --quiet
    git reset --hard @{upstream}
fi



task --output=prefixed --dir=/opt/ringgem install-mylime-on-linux
