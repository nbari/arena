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

mysql:

make install PREFIX=/arena/db/mysql/mysql-56
