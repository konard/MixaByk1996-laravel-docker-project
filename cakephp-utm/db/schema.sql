CREATE TABLE IF NOT EXISTS `utm_data` (
    `id`       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `source`   VARCHAR(255) NOT NULL,
    `medium`   VARCHAR(255) NOT NULL,
    `campaign` VARCHAR(255) NOT NULL,
    `content`  VARCHAR(255) DEFAULT NULL,
    `term`     VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_source`   (`source`),
    INDEX `idx_medium`   (`medium`),
    INDEX `idx_campaign` (`campaign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
