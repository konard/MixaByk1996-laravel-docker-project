<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo h($title_for_layout); ?></title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Courier New', Courier, monospace; background: #f5f5f5; color: #333; padding: 20px; }
        h1 { margin-bottom: 20px; font-size: 1.5rem; color: #222; }
        .utm-tree { background: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 16px; }
        .tree-node { line-height: 1.8; }
        .level-0 { font-weight: bold; color: #1a1a1a; }
        .level-1 { padding-left: 1em; color: #2c5282; }
        .level-2 { padding-left: 2em; color: #276749; }
        .level-3 { padding-left: 3em; color: #744210; }
        .level-4 { padding-left: 4em; color: #63171b; }
        .null-value { color: #999; font-style: italic; }
        .pagination { margin-top: 20px; display: flex; gap: 8px; align-items: center; }
        .pagination a, .pagination span {
            display: inline-block; padding: 6px 12px;
            border: 1px solid #ccc; border-radius: 4px;
            text-decoration: none; color: #333; background: #fff;
        }
        .pagination a:hover { background: #e8e8e8; }
        .pagination .current { background: #2c5282; color: #fff; border-color: #2c5282; }
        .pagination .disabled { color: #aaa; cursor: not-allowed; }
        .stats-info { color: #666; font-size: 0.9rem; margin-bottom: 12px; }
        .empty { color: #999; font-style: italic; }
    </style>
</head>
<body>
    <h1><?php echo h($title_for_layout); ?></h1>
    <?php echo $content_for_layout; ?>
</body>
</html>
