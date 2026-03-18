# Инструкция по развертыванию на Production

## Предварительные требования

### Серверные требования
- **ОС**: Ubuntu 20.04/22.04 LTS или Debian 11+
- **RAM**: минимум 4 GB (рекомендуется 8 GB)
- **CPU**: 2+ ядра
- **Диск**: 50+ GB SSD
- **Docker**: версия 24.0+
- **Docker Compose**: версия 2.0+

### Необходимые доступы
- Avito API credentials (client_id, client_secret)
- SMTP-сервер для отправки email
- Доменное имя с SSL-сертификатом (для production)

---

## Шаг 1: Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo apt install docker-compose-plugin -y

# Перелогиниться для применения группы docker
exit
```

---

## Шаг 2: Клонирование проекта

```bash
# Клонирование репозитория
git clone https://github.com/MixaByk1996/laravel-docker-project.git
cd laravel-docker-project
```

---

## Шаг 3: Настройка окружения

```bash
# Создание файла конфигурации
cp .env.example .env
```

Отредактируйте `.env` файл:

```bash
nano .env
```

### Обязательные настройки для Production:

```env
# Database - ОБЯЗАТЕЛЬНО измените пароль!
POSTGRES_USER=avito_bot
POSTGRES_PASSWORD=<СИЛЬНЫЙ_СЛУЧАЙНЫЙ_ПАРОЛЬ>
POSTGRES_DB=avito_bot_db
DATABASE_URL=postgresql+asyncpg://avito_bot:<СИЛЬНЫЙ_СЛУЧАЙНЫЙ_ПАРОЛЬ>@db:5432/avito_bot_db

# Redis
REDIS_URL=redis://redis:6379/0

# Avito API - получите в личном кабинете Avito
AVITO_CLIENT_ID=<ваш_client_id>
AVITO_CLIENT_SECRET=<ваш_client_secret>
AVITO_API_BASE_URL=https://api.avito.ru

# SMTP - настройки вашего email-провайдера
SMTP_HOST=smtp.yandex.ru
SMTP_PORT=465
SMTP_USER=your-email@yandex.ru
SMTP_PASSWORD=<пароль_приложения>
SMTP_FROM_EMAIL=your-email@yandex.ru
SMTP_FROM_NAME=Avito Bot

# App - ОБЯЗАТЕЛЬНО измените SECRET_KEY!
SECRET_KEY=<СЛУЧАЙНАЯ_СТРОКА_64_СИМВОЛА>
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false

# Frontend
VITE_API_URL=/api/v1
```

### Генерация SECRET_KEY:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## Шаг 4: Настройка Nginx с SSL (для Production)

Создайте файл `nginx/production.conf`:

```bash
mkdir -p nginx
cat > nginx/production.conf << 'EOF'
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:5173;
}

server {
    listen 80;
    server_name your-domain.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.ru;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # API requests
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF
```

---

## Шаг 5: Создание docker-compose.production.yml

```bash
cat > docker-compose.production.yml << 'EOF'
version: "3.8"

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-avito_bot}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB:-avito_bot_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-avito_bot}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  celery_worker:
    build: ./backend
    command: celery -A app.core.celery_app worker --loglevel=info --concurrency=4
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  celery_beat:
    build: ./backend
    command: celery -A app.core.celery_app beat --loglevel=info
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.production
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/production.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF
```

---

## Шаг 6: Создание Production Dockerfile для Frontend

```bash
cat > frontend/Dockerfile.production << 'EOF'
FROM node:20-alpine as build

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
```

```bash
cat > frontend/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://backend:8000;
        }
    }
}
EOF
```

---

## Шаг 7: Запуск приложения

```bash
# Сборка и запуск всех сервисов
docker compose -f docker-compose.production.yml up -d --build

# Проверка статуса
docker compose -f docker-compose.production.yml ps

# Просмотр логов
docker compose -f docker-compose.production.yml logs -f
```

---

## Шаг 8: Применение миграций БД

```bash
# Выполнение миграций
docker compose -f docker-compose.production.yml exec backend alembic upgrade head
```

---

## Шаг 9: Проверка работоспособности

```bash
# Проверка API
curl http://localhost/api/health

# Проверка доступности Swagger документации
curl http://localhost/api/docs
```

---

## Резервное копирование

### Настройка автоматического бэкапа БД

```bash
# Создание скрипта бэкапа
cat > /opt/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

docker compose -f /path/to/project/docker-compose.production.yml exec -T db \
    pg_dump -U avito_bot avito_bot_db | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Удаление бэкапов старше 7 дней
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
EOF

chmod +x /opt/backup-db.sh

# Добавление в cron (ежедневно в 3:00)
echo "0 3 * * * /opt/backup-db.sh" | crontab -
```

---

## Мониторинг

### Просмотр логов

```bash
# Все сервисы
docker compose -f docker-compose.production.yml logs -f

# Конкретный сервис
docker compose -f docker-compose.production.yml logs -f backend
docker compose -f docker-compose.production.yml logs -f celery_worker
```

### Перезапуск сервисов

```bash
# Перезапуск всего
docker compose -f docker-compose.production.yml restart

# Перезапуск конкретного сервиса
docker compose -f docker-compose.production.yml restart backend
```

---

## Обновление приложения

```bash
# Получение последних изменений
git pull origin master

# Пересборка и перезапуск
docker compose -f docker-compose.production.yml up -d --build

# Применение новых миграций (если есть)
docker compose -f docker-compose.production.yml exec backend alembic upgrade head
```

---

## Устранение неполадок

### Проблема: База данных не запускается
```bash
docker compose -f docker-compose.production.yml logs db
# Проверьте права на volume
```

### Проблема: Backend не отвечает
```bash
docker compose -f docker-compose.production.yml logs backend
# Проверьте DATABASE_URL в .env
```

### Проблема: Celery задачи не выполняются
```bash
docker compose -f docker-compose.production.yml logs celery_worker
docker compose -f docker-compose.production.yml logs celery_beat
# Проверьте REDIS_URL в .env
```

---

## Рекомендации по безопасности

1. **Используйте сильные пароли** для PostgreSQL и SECRET_KEY
2. **Ограничьте доступ** к портам 5432 (PostgreSQL) и 6379 (Redis) через firewall
3. **Настройте SSL** для HTTPS
4. **Регулярно обновляйте** Docker образы
5. **Настройте мониторинг** и алерты
6. **Делайте регулярные бэкапы** базы данных

```bash
# Настройка firewall (UFW)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
