<?php
if (!defined('DS')) {
    define('DS', DIRECTORY_SEPARATOR);
}

if (!defined('ROOT')) {
    define('ROOT', dirname(dirname(dirname(__FILE__))));
}

if (!defined('APP_DIR')) {
    define('APP_DIR', basename(dirname(dirname(__FILE__))));
}

define('WEBROOT_DIR', basename(dirname(__FILE__)));
define('WWW_ROOT', dirname(__FILE__) . DS);

if (!defined('CAKE_CORE_INCLUDE_PATH')) {
    define('CAKE_CORE_INCLUDE_PATH', ROOT);
}

if (!include(CAKE_CORE_INCLUDE_PATH . DS . 'lib' . DS . 'Cake' . DS . 'bootstrap.php')) {
    $corePath = CAKE_CORE_INCLUDE_PATH . DS . 'lib';
    if (function_exists('ini_set')) {
        ini_set('include_path', $corePath . PATH_SEPARATOR . ini_get('include_path'));
    }
    if (!include($corePath . DS . 'Cake' . DS . 'bootstrap.php')) {
        trigger_error('CakePHP core could not be found. Make sure CakePHP exists.', E_USER_ERROR);
    }
}

App::uses('Dispatcher', 'Routing');
$Dispatcher = new Dispatcher();
$Dispatcher->dispatch(
    new CakeRequest(),
    new CakeResponse()
);
