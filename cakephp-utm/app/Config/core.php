<?php
Configure::write('debug', 0);
Configure::write('App.encoding', 'UTF-8');
Configure::write('App.base', false);
Configure::write('App.baseUrl', false);
Configure::write('App.dir', 'app');
Configure::write('App.webroot', 'webroot');
Configure::write('App.www_root', WWW_ROOT);
Configure::write('App.fullBaseUrl', 'http://localhost');
Configure::write('App.imageBaseUrl', 'img/');
Configure::write('App.cssBaseUrl', 'css/');
Configure::write('App.jsBaseUrl', 'js/');
Configure::write('App.paths.plugins', array(APP . 'Plugin' . DS));
Configure::write('App.paths.views', array(APP . 'View' . DS));
Configure::write('App.paths.shells', array(APP . 'Console' . DS . 'Command' . DS));
Configure::write('Security.salt', 'utm_app_salt_value_change_in_production');
Configure::write('Security.cipherSeed', '12345678901234567890123456789012');
Configure::write('Session', array(
    'defaults' => 'php',
));
Configure::write('Cache.disable', true);
