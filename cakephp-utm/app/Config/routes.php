<?php
Router::connect('/', array('controller' => 'statistics', 'action' => 'index'));
Router::connect('/statistics/utm/list', array('controller' => 'statistics', 'action' => 'utm_list'));
Router::connect('/statistics/utm/list/:page', array('controller' => 'statistics', 'action' => 'utm_list'), array('pass' => array('page'), 'page' => '[0-9]+'));
CakePlugin::routes();
require CAKE . 'Config' . DS . 'routes.php';
