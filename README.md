arena
=====

Deployment schema for microservices / sites using host shared binaries:

    /arena
    |--service-name-1
    |  |--releases
    |  |  `--ISO8601-time # (date -Iseconds)
    |  |--run.yml
    |  |--@current
    |  `--logs
    `--service-name-2
       |--releases
       |  `--ISO8601-time
       |--run.yml
       |--@current
       `--logs

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
