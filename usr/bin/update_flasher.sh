#!/bin/sh

LED_ZIGBEE=86
LED_BERG_CLOUD=87
LED_ETHERNET=88

echo $LED_ZIGBEE > /sys/class/gpio/export
echo $LED_BERG_CLOUD > /sys/class/gpio/export
echo $LED_ETHERNET > /sys/class/gpio/export

echo "out" > /sys/class/gpio/gpio$LED_ZIGBEE/direction
echo "out" > /sys/class/gpio/gpio$LED_BERG_CLOUD/direction
echo "out" > /sys/class/gpio/gpio$LED_ETHERNET/direction

echo "1" > /sys/class/gpio/gpio$LED_ZIGBEE/value
echo "1" > /sys/class/gpio/gpio$LED_BERG_CLOUD/value
echo "1" > /sys/class/gpio/gpio$LED_ETHERNET/value

LOOP=1
PIDFILE=/tmp/update_flasher.pid

start_flash_loop() {

    while [ 1 ]; do
      #echo "LOOP $LOOP"
      usleep 100

      if [ $LOOP -eq 1 ]; then
        echo "0" > /sys/class/gpio/gpio$LED_ZIGBEE/value
      fi
      if [ $LOOP -eq 10 ]; then
        echo "1" > /sys/class/gpio/gpio$LED_ZIGBEE/value
      fi

      if [ $LOOP -eq 10 ]; then
          echo "0" > /sys/class/gpio/gpio$LED_BERG_CLOUD/value
      fi
      if [ $LOOP -eq 20 ]; then
          echo "1" > /sys/class/gpio/gpio$LED_BERG_CLOUD/value
      fi

      if [ $LOOP -eq 20 ]; then
          echo "0" > /sys/class/gpio/gpio$LED_ETHERNET/value
      fi
      if [ $LOOP -eq 30 ]; then
          echo "1" > /sys/class/gpio/gpio$LED_ETHERNET/value
      fi

      LOOP=`expr $LOOP + 1`

      if [ $LOOP -eq 40 ]; then
        LOOP=1
      fi
    done

exit 0
}

stop_flash_loop() {
    if [ -e $PIDFILE ]; then
        PID=`cat $PIDFILE`
        kill $PID
    
        echo "1" > /sys/class/gpio/gpio$LED_ZIGBEE/value
        echo "1" > /sys/class/gpio/gpio$LED_BERG_CLOUD/value
        echo "1" > /sys/class/gpio/gpio$LED_ETHERNET/value
        exit 0
    fi
    
    exit 1;
}

if [ $1 == "start" ]; then
    start_flash_loop &
    echo $! > $PIDFILE
fi

if [ $1 == "stop" ]; then
    stop_flash_loop
fi
