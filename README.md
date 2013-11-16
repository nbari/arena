arena
=====

Deployment schema for web applications and services

    arena
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


poudriere jails -c -j 9amd64 -v stable/9 -a amd64 -m svn -J 4
