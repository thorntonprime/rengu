#!/bin/bash
# 

RETVAL=0

# Source function library.
. /etc/rc.d/init.d/functions


usage ()
{
	echo $"Usage: $0 {start|stop|status|restart|condrestart}" 1>&2
	RETVAL=2
}

stop ()
{
    celery-3 multi stop 10 \
        --pidfile=tmp/celery-%n.pid
}

status ()
{
    celery-3 multi show 10 \
        --pidfile=tmp/celery-%n.pid
}

restart () 
{
    celery-3 multi restart 10 \
        --pidfile=tmp/celery-%n.pid
}

start () 
{
    celery-3 multi start 10 \
        -A rengu \
        -f tmp/%n-%i.log \
	-l info -c4 \
        --pidfile=tmp/celery-%n.pid
}

case "$1" in
    stop) stop ;;
    status) status ;;
    start) start ;;
    restart|reload|force-reload) restart ;;
    *) usage ;;
esac

exit $RETVAL

