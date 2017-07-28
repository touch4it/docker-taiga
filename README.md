# What is Taiga?

Taiga is a project management platform for startups and agile developers & designers who want a simple, beautiful tool that makes work truly enjoyable.

> [taiga.io](https://taiga.io)

# How to use this image

Taiga needs a database (PostgreSQL) and optionally `taiga-events`, `rabbitmq` and `redis` for real-time events. You can use following `docker-compose.yml` configurations to manage the dependencies:

## Without taiga-events

```
version: '2'
services:
  taiga:
    image: touch4it/taiga
    environment:
      TAIGA_DB_PASSWORD: password
      TAIGA_EMAIL_ADDR: noreply@example.com
      TAIGA_EMAIL_ENABLED: 'true'
      TAIGA_EMAIL_HOST: smtp.example.com
      TAIGA_EMAIL_PORT: '587'
      TAIGA_EMAIL_USER: user
      TAIGA_EMAIL_PASS: pass
      TAIGA_EMAIL_USE_TLS: 'true'
      TAIGA_HOSTNAME: taiga.example.com
      TAIGA_PUBLIC_REGISTER_ENABLED: 'true'
      TAIGA_SSL: 'true'
    volumes:
    - /volumes/taiga/media:/usr/src/taiga-back/media
  postgres:
    image: postgres:9.6-alpine
    environment:
      POSTGRES_DB: taiga
      POSTGRES_PASSWORD: password
      POSTGRES_USER: taiga
    volumes:
    - /volumes/taiga/pgdata:/var/lib/postgresql/data
    expose:
    - '5432'
```

## With taiga-events

```
version: '2'
services:
  taiga:
    image: touch4it/taiga
    environment:
      TAIGA_HOSTNAME: taiga.example.com
      TAIGA_PUBLIC_REGISTER_ENABLED: 'true'
      TAIGA_EVENTS_ENABLED: 'true'
      TAIGA_CELERY_ENABLED: 'true'
      TAIGA_DB_PASSWORD: password
      TAIGA_SECRET_KEY: secret
      TAIGA_EMAIL_ADDR: noreply@example.com
      TAIGA_EMAIL_ENABLED: 'true'
      TAIGA_EMAIL_HOST: smtp.example.com
      TAIGA_EMAIL_PORT: '587'
      TAIGA_EMAIL_USER: user
      TAIGA_EMAIL_PASS: pass
      TAIGA_EMAIL_USE_TLS: 'true'
      TAIGA_SSL: 'true'
    volumes:
    - /volumes/taiga/media:/usr/src/taiga-back/media
  events:
    image: touch4it/taiga-events
    environment:
      TAIGA_SECRET_KEY: secret
  rabbit:
    image: rabbitmq:3.6-alpine
  redis:
    image: redis:3.2-alpine
  postgres:
    image: postgres:9.6-alpine
    environment:
      POSTGRES_DB: taiga
      POSTGRES_PASSWORD: password
      POSTGRES_USER: taiga
    volumes:
    - /volumes/taiga/pgdata:/var/lib/postgresql/data
    expose:
    - '5432'
```

## Configuration options

The following configuration options are available:

### Basic configuration

| Env. variable                 | Default value                                    | Description                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------|
| TAIGA_HOSTNAME                | localhost                                        | Hostname for (API) URLs                               |
| TAIGA_SSL                     | false                                            | Use HTTPS / WSS in URLs                               |
| TAIGA_PUBLIC_REGISTER_ENABLED | false                                            | Enable/disable public registrations                   |
| TAIGA_SECRET_KEY              | mysecret                                         | Secret key for API/socket access                      |
| TAIGA_DEBUG                   | false                                            | More debug info in logs                               |
| TAIGA_TEMPLATE_DEBUG          | false                                            | More debug info for templates                         |

### Database configuration

| Env. variable                 | Default value                                    | Description                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------|
| TAIGA_DB_HOST                 | postgres                                         | PostgreSQL database hostname                          |
| TAIGA_DB_NAME                 | taiga                                            | PostgreSQL database name                              |
| TAIGA_DB_USER                 | taiga                                            | PostgreSQL database user                              |
| TAIGA_DB_PASSWORD             | taiga                                            | PostgreSQL database password                          |

### E-mail configuration

| Env. variable                 | Default value                                    | Description                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------|
| TAIGA_EMAIL_ENABLED           | false                                            | Enable sending e-mails                                |
| TAIGA_EMAIL_HOST              | localhost                                        | SMTP hostname                                         |
| TAIGA_EMAIL_PORT              | 25                                               | SMTP port                                             |
| TAIGA_EMAIL_USER              |                                                  | SMTP user                                             |
| TAIGA_EMAIL_PASS              |                                                  | SMTP password                                         |
| TAIGA_EMAIL_USE_TLS           | false                                            | SMTP STARTTLS                                         |

### Events and asynchronous tasks configutation

| Env. variable                 | Default value                                    | Description                                           |
|-------------------------------|--------------------------------------------------|-------------------------------------------------------|
| TAIGA_EVENTS_ENABLED          | false                                            | Enable/disable taiga-events - see docker-compose.yml  |
| TAIGA_CELERY_ENABLED          | false                                            | Enable Celery - asynchronous task/job queue           |
| TAIGA_EVENTS_PUSH_BACKEND     | taiga.events.backends.rabbitmq.EventsPushBackend | Backend for taiga-events (usually rabbitmq)           |
| TAIGA_EVENTS_PUSH_BACKEND_URL | amqp://guest:guest@rabbit:5672//                 | URL for taiga-events backend                          |
