FROM php:7.4-apache

RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    unzip \
    curl \
    default-libmysqlclient-dev \
    && docker-php-ext-install pdo pdo_mysql mysqli \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite

COPY apache.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /var/www/html

RUN curl -sL https://github.com/cakephp/cakephp/archive/refs/tags/2.10.24.tar.gz \
    | tar -xz --strip-components=1 -C /var/www/html

COPY app/ /var/www/html/app/

RUN mkdir -p /var/www/html/app/tmp/cache/models \
             /var/www/html/app/tmp/cache/persistent \
             /var/www/html/app/tmp/cache/views \
             /var/www/html/app/tmp/logs \
    && chmod -R 777 /var/www/html/app/tmp

EXPOSE 80
