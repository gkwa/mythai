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







apt-get install --assume-yes unzip curl





curl -fsSL https://raw.githubusercontent.com/taylormonacelli/ringgem/master/install-go-task-on-linux.sh | sudo bash
curl -Lo /tmp/ringgem-master.zip https://github.com/taylormonacelli/ringgem/archive/refs/heads/master.zip
unzip /tmp/ringgem-master.zip -d /tmp/ringgem
task --output=prefixed --dir=/tmp/ringgem/ringgem-master --verbose install-git-on-linux

mkdir -p /opt/ringgem
git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git init --quiet
git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git remote add origin https://github.com/taylormonacelli/ringgem.git
git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git pull origin master
git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git branch --set-upstream-to=origin/master master
git --git-dir=/opt/ringgem/.git pull

rm -rf /tmp/ringgem /tmp/ringgem-master.zip
