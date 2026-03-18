# UTM Data Visualizer — CakePHP 2

A mini-application built on CakePHP 2 that processes and displays UTM tracking data as a nested tree structure.

## Requirements

- PHP 5.6+ (or use Docker)
- MySQL 5.6+
- Apache with `mod_rewrite` enabled

## Quick Start (Docker)

```bash
docker-compose up --build
```

Open http://localhost:8080/statistics/utm/list

## Manual Setup

### 1. Database

Create the database and run the schema + seed:

```bash
mysql -u root -p < db/schema.sql
mysql -u root -p utm_db < db/seed.sql
```

### 2. CakePHP 2 Core

Download CakePHP 2.x and place it so the directory structure is:

```
cakephp-utm/
├── app/
├── lib/         ← CakePHP core goes here (lib/Cake/...)
└── ...
```

```bash
curl -sL https://github.com/cakephp/cakephp/archive/refs/tags/2.10.24.tar.gz \
  | tar -xz --strip-components=1
```

### 3. Environment Variables

```bash
export DB_HOST=localhost
export DB_USER=utm_user
export DB_PASS=utm_pass
export DB_NAME=utm_db
```

Or edit `app/Config/bootstrap.php` directly.

### 4. Web Server

Point your Apache `DocumentRoot` to `app/webroot/` and enable `mod_rewrite`.

## Project Structure

```
cakephp-utm/
├── app/
│   ├── Config/
│   │   ├── bootstrap.php   # DB env vars
│   │   ├── core.php        # CakePHP settings
│   │   ├── database.php    # DB connection
│   │   └── routes.php      # URL routing
│   ├── Controller/
│   │   ├── AppController.php
│   │   └── StatisticsController.php
│   ├── Model/
│   │   ├── AppModel.php
│   │   └── UtmData.php     # Tree query with pagination
│   ├── View/
│   │   ├── Layouts/default.ctp
│   │   └── Statistics/utm_list.ctp
│   └── webroot/
│       ├── .htaccess
│       └── index.php
├── db/
│   ├── schema.sql          # Table definition
│   └── seed.sql            # Example data
├── apache.conf
├── docker-compose.yml
└── Dockerfile
```

## Database Schema

```sql
CREATE TABLE utm_data (
    id       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    source   VARCHAR(255) NOT NULL,
    medium   VARCHAR(255) NOT NULL,
    campaign VARCHAR(255) NOT NULL,
    content  VARCHAR(255) DEFAULT NULL,
    term     VARCHAR(255) DEFAULT NULL
);
```

## Page: /statistics/utm/list

Displays UTM data as a nested tree:

```
google
....cpc
........summer
............banner
................video
........winter
............delta
................NULL
```

Pagination shows **20 sources per page**.

## Example Data (from spec)

| source | medium | campaign | content | term  |
|--------|--------|----------|---------|-------|
| google | cpc    | summer   | banner  | video |
| google | cpc    | winter   | delta   | NULL  |
