<div class="stats-info">
    Total sources: <?php echo $total; ?> &nbsp;|&nbsp;
    Page <?php echo $page; ?> of <?php echo $totalPages; ?>
    (<?php echo $perPage; ?> sources per page)
</div>

<div class="utm-tree">
<?php if (empty($tree)): ?>
    <p class="empty">No UTM data found.</p>
<?php else: ?>
<?php foreach ($tree as $source => $mediums): ?>
    <div class="tree-node level-0"><?php echo h($source); ?></div>
    <?php foreach ($mediums as $medium => $campaigns): ?>
    <div class="tree-node level-1">....<?php echo h($medium); ?></div>
        <?php foreach ($campaigns as $campaign => $contents): ?>
        <div class="tree-node level-2">........<?php echo h($campaign); ?></div>
            <?php foreach ($contents as $contentKey => $terms): ?>
            <?php $contentDisplay = ($contentKey === '__NULL__') ? 'NULL' : $contentKey; ?>
            <div class="tree-node level-3">............<span <?php echo ($contentKey === '__NULL__') ? 'class="null-value"' : ''; ?>><?php echo h($contentDisplay); ?></span></div>
                <?php if (!empty($terms)): ?>
                    <?php foreach ($terms as $term): ?>
                    <div class="tree-node level-4">................<?php echo h($term); ?></div>
                    <?php endforeach; ?>
                <?php endif; ?>
            <?php endforeach; ?>
        <?php endforeach; ?>
    <?php endforeach; ?>
<?php endforeach; ?>
<?php endif; ?>
</div>

<?php if ($totalPages > 1): ?>
<div class="pagination">
    <?php if ($page > 1): ?>
        <a href="/statistics/utm/list/<?php echo $page - 1; ?>">&#8592; Prev</a>
    <?php else: ?>
        <span class="disabled">&#8592; Prev</span>
    <?php endif; ?>

    <?php
    $start = max(1, $page - 2);
    $end   = min($totalPages, $page + 2);
    for ($i = $start; $i <= $end; $i++):
    ?>
        <?php if ($i === $page): ?>
            <span class="current"><?php echo $i; ?></span>
        <?php else: ?>
            <a href="/statistics/utm/list/<?php echo $i; ?>"><?php echo $i; ?></a>
        <?php endif; ?>
    <?php endfor; ?>

    <?php if ($page < $totalPages): ?>
        <a href="/statistics/utm/list/<?php echo $page + 1; ?>">Next &#8594;</a>
    <?php else: ?>
        <span class="disabled">Next &#8594;</span>
    <?php endif; ?>
</div>
<?php endif; ?>
