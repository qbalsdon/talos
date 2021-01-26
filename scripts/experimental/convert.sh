#!/bin/sh
FILE=pattern.event
while read line; do
  #HEX=${line##* }
  #INT=$((16#$HEX))
  #echo "${line/$HEX/$INT}"    

  EVENT=$(echo $line | awk '{print $2}')
  NUM1=$(echo $line | awk '{print $3}')
  NUM2=$(echo $line | awk '{print $4}')
  NUM3=$(echo $line | awk '{print $5}')
  
  NUM1=$((16#$NUM1))
  NUM2=$((16#$NUM2))
  NUM3=$((16#$NUM3))


  echo "sendevent $EVENT $NUM1 $NUM2 $NUM3"

done <$FILE
