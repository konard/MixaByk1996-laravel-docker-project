<?php
App::uses('AppController', 'Controller');

class StatisticsController extends AppController {
    public $uses = array('UtmData');

    public function index() {
        $this->redirect(array('action' => 'utm_list'));
    }

    public function utm_list($page = 1) {
        $page = max(1, (int) $page);
        $result = $this->UtmData->getPaginatedTree($page);

        $this->set('tree',       $result['tree']);
        $this->set('page',       $result['page']);
        $this->set('totalPages', $result['totalPages']);
        $this->set('total',      $result['total']);
        $this->set('perPage',    $result['perPage']);
        $this->set('title_for_layout', 'UTM Statistics');
    }
}
