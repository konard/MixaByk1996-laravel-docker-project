<?php
App::uses('AppModel', 'Model');

class UtmData extends AppModel {
    public $name = 'UtmData';
    public $useTable = 'utm_data';

    public $validate = array(
        'source' => array(
            'notEmpty' => array(
                'rule'    => 'notBlank',
                'message' => 'Source is required',
            ),
        ),
        'medium' => array(
            'notEmpty' => array(
                'rule'    => 'notBlank',
                'message' => 'Medium is required',
            ),
        ),
        'campaign' => array(
            'notEmpty' => array(
                'rule'    => 'notBlank',
                'message' => 'Campaign is required',
            ),
        ),
    );

    public function getPaginatedTree($page = 1, $perPage = 20) {
        $offset = ($page - 1) * $perPage;

        $totalSources = $this->query(
            "SELECT COUNT(DISTINCT source) AS total FROM utm_data"
        );
        $total = (int) $totalSources[0][0]['total'];

        $sources = $this->query(
            "SELECT DISTINCT source FROM utm_data ORDER BY source LIMIT ? OFFSET ?",
            array($perPage, $offset)
        );
        $sourceList = array_column(array_column($sources, 'utm_data'), 'source');

        if (empty($sourceList)) {
            return array(
                'tree'       => array(),
                'total'      => $total,
                'page'       => $page,
                'perPage'    => $perPage,
                'totalPages' => (int) ceil($total / $perPage),
            );
        }

        $placeholders = implode(',', array_fill(0, count($sourceList), '?'));
        $rows = $this->query(
            "SELECT source, medium, campaign, content, term
             FROM utm_data
             WHERE source IN ($placeholders)
             ORDER BY source, medium, campaign, content, term",
            $sourceList
        );

        $tree = array();
        foreach ($rows as $row) {
            $r = $row['utm_data'];
            $src  = $r['source'];
            $med  = $r['medium'];
            $camp = $r['campaign'];
            $cont = isset($r['content']) ? $r['content'] : null;
            $term = isset($r['term'])    ? $r['term']    : null;

            if (!isset($tree[$src])) {
                $tree[$src] = array();
            }
            if (!isset($tree[$src][$med])) {
                $tree[$src][$med] = array();
            }
            if (!isset($tree[$src][$med][$camp])) {
                $tree[$src][$med][$camp] = array();
            }
            $contKey = ($cont === null) ? '__NULL__' : $cont;
            if (!isset($tree[$src][$med][$camp][$contKey])) {
                $tree[$src][$med][$camp][$contKey] = array();
            }
            if ($term !== null && !in_array($term, $tree[$src][$med][$camp][$contKey])) {
                $tree[$src][$med][$camp][$contKey][] = $term;
            }
        }

        return array(
            'tree'       => $tree,
            'total'      => $total,
            'page'       => $page,
            'perPage'    => $perPage,
            'totalPages' => (int) ceil($total / $perPage),
        );
    }
}
