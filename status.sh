#!/bin/sh

status=`cat status.cam`

if [ $1 = "start" ]; then
  sudo motion start && echo 1 > status.cam
fi

if [ $1 = "stop" ]; then
  echo "0" > status.cam
  sudo kill -9 `ps -ef | grep motion | grep root | awk '{print $2}'` && echo "0" > status.cam
fi


