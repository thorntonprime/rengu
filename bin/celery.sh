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
    celery-3 multi stop
    rm tmp/celery-*.pid
}

status ()
{
    celery-3 multi show
}

start () 
{
    celery-3 multi start 10 \
        -A rengu \
        -l info -c4 \
        -f %n-%i.log \
        --pidfile=tmp/celery-%n.pid
}

case "$1" in
    stop) stop ;;
    status) status ;;
    start) start ;;
    restart|reload|force-reload) restart ;;
    # condrestart) condrestart ;;
    *) usage ;;
esac

exit $RETVAL

