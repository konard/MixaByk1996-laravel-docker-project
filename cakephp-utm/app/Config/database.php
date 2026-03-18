<?php
class DATABASE_CONFIG {
    public $default = array(
        'datasource' => 'Database/Mysql',
        'persistent' => false,
        'host'       => DB_HOST,
        'login'      => DB_USER,
        'password'   => DB_PASS,
        'database'   => DB_NAME,
        'prefix'     => '',
        'encoding'   => 'utf8',
    );
}
