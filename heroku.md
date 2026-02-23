# Heroku CLI Reference

## App URLs

| App | URL |
|-----|-----|
| Backend API | https://formation-electro-api-83d5f74e9e09.herokuapp.com |
| Frontend | https://formation-electro-front-ae72b687cedd.herokuapp.com |

### Health Check

```bash
curl https://formation-electro-api-83d5f74e9e09.herokuapp.com/health
```

---

## Authentication

### Re-authenticate (Session Expired)

```bash
heroku logout
heroku login
```

> Opens a browser window to complete login.

### Verify Login

```bash
heroku auth:whoami
heroku auth:token
```

### Headless / No Browser Environment

```bash
heroku login -i
```

> Prompts for email and password directly in the terminal.

---

## Dyno Management

### Restart

```bash
heroku restart --app formation-electro-api
```

```bash
# Restart a specific dyno type
heroku restart web --app formation-electro-api
```

### Stop (Scale Down to 0)

```bash
heroku ps:scale web=0 --app formation-electro-api
```

### Start (Scale Back Up)

```bash
heroku ps:scale web=1 --app formation-electro-api
```

### Check Status

```bash
heroku ps --app formation-electro-api
```

### View Logs

```bash
heroku logs --tail --app formation-electro-api
```

### Find Your App Name

```bash
heroku apps
```

> **Note:** Heroku has no direct stop/start command. Stopping is done by scaling dynos to `0`, starting by scaling back to `1` or more.

---

## Config Vars

### View All Config Vars

```bash
heroku config --app formation-electro-api
```

### Set a Config Var

```bash
heroku config:set KEY=value --app formation-electro-api
```

### Set Multiple Config Vars

```bash
heroku config:set KEY1=value1 KEY2=value2 --app formation-electro-api
```

### Unset a Config Var

```bash
heroku config:unset KEY --app formation-electro-api
```

### Unset Multiple Config Vars

```bash
heroku config:unset KEY1 KEY2 KEY3 --app formation-electro-api
```

### Fix CORS JSON Parse Error

```bash
heroku config:unset CORS_ORIGINS CORS_ALLOW_METHODS CORS_ALLOW_HEADERS --app formation-electro-api
```

> Removes empty CORS vars so pydantic-settings falls back to code defaults `["*"]`.

---

## Releases & Logs

### List All Releases

```bash
heroku releases --app formation-electro-api
```

### View Latest Release Log

```bash
heroku releases:output --app formation-electro-api
```

### View Last 200 Log Lines

```bash
heroku logs --app formation-electro-api -n 200
```

### Stream Live Logs

```bash
heroku logs --tail --app formation-electro-api
```
