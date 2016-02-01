arena
=====

For microservices

    /arena
    |--service-name-1
    |  |--home
    |  |--home.ISO8601-time
    `--service-name-2
       |--home
       `--home.ISO8601-time



Deployment schema for web applications and services

    /arena
    |--db
    |  |--mysql
    |  `--redis
    |--home
    |  |--apps
    |  `--sites
    |--logs
    |--root
    |  |--etc
    |  |--bin
    |  `--sbin
    |--sandbox
    |--src
    `--supervise
       |--memcached
       |  `--log
       |--mysql
       |  `--log
       `--redis
          `-- log



compiling ports
---------------

make install PREFIX=/arena/root


poudriere jails -c -j 9amd64 -v 9.2-RELEASE -a amd64

poudriere jails -c -j 9amd64 -v stable/9 -a amd64 -m svn



    poudriere options -c www/nginx

Or if you want to configure all the options all the ports will be built with:

    poudriere options -c `cat /usr/local/etc/poudriere-list`

Build:

    poudriere bulk -j 9amd64 www/nginx

    poudriere bulk -f ~/mylist2 -j 9amd64

To update the repository:

    poudriere ports -u # this update your default ports tree
    poudriere bulk -f ~/mylist2 -j 9amd64 -k



The global make.conf looks like:

    WITH_PKGNG=yes
    NO_PROFILE=true
    NO_X=true
    WITHOUT_X11=yes
    PREFIX=/arena/root
