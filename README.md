# Agromant

Recently I was trying to get a better paying job, but I got quite a small
amount of public projects to show, cause they're all commercial or under NDA :3

So I decided to create a public project, also commercial lol, which would be
useful for me and possibly for others. Inspired by my GF's plant collection,
and our CEO's frozen project about detecting leaf diseases. The core idea is to
create a telegram bot that would help people to take care of their plants

## Stack

- Python 3.13
- FastAPI
- MongoDB

Depends on ProxyAPI service to make available access to ChatGPT API in Russia
and Yookassa API for payments

## Installation

### Docker

With environment containers, ready to use:

```bash
docker compose --profile environment up -d
```

Only application container:

```bash
docker compose --profile production up -d
```

Also you need to create `.env` file in `bot` directory with specified variables

```env

### Manual

- Install Python 3.13
- Install dependencies
  
```bash
cd bot
pip install -r requirements.txt
```

- Create `.env` file in `bot` directory with the specified variables
- Run the bot

```bash
python main.py
```

### Environment variables

- `TG_BOT_API_KEY` - Telegram bot API key
- `PROXY_AI_API_KEY` - ProxyAPI access token
- `MONGO_HOST` - MongoDB host
- `MONGO_PORT` - MongoDB port
- `MONGO_DATABASE` - MongoDB database name
- `MONGO_ROOT_USERNAME` - MongoDB root username
- `MONGO_ROOT_PASSWORD` - MongoDB root password
- `YOOKASSA_SHOP_ID` - Yookassa shop ID
- `YOOKASSA_SECRET_KEY` - Yookassa secret key

If you also use MongoExpress, you need to set the following variables:

- `ME_CONFIG_MONGODB_ADMINUSERNAME`- MongoDB admin username
- `ME_CONFIG_MONGODB_ADMINPASSWORD`- MongoDB admin password
- `ME_CONFIG_MONGODB_SERVER` - MongoDB host
- `ME_CONFIG_MONGODB_PORT` - MongoDB port
- `ME_CONFIG_OPTIONS_AUTH_SOURCE` - Authentication source, usually `admin`
- `ME_CONFIG_BASICAUTH_USERNAME` - Mongo Express username
- `ME_CONFIG_BASICAUTH_PASSWORD` - Mongo Express password

Example `.env` file:

```env
# Bot settings

TG_BOT_API_KEY=123456789:ABCdefGHIjklMNOpQRStuvWXYz0123456789
PROXY_AI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz1234567890
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_ROOT_USERNAME=example
MONGO_ROOT_PASSWORD=1234567890
MONGO_DATABASE=example_db
YOOKASSA_SHOP_ID=123456789
YOOKASSA_SECRET_KEY=live_abcdefghijklmnopqrstuvwxyz1234567890

# Mongo Express settings

ME_CONFIG_MONGODB_ADMINUSERNAME=${MONGO_ROOT_USERNAME}
ME_CONFIG_MONGODB_ADMINPASSWORD=${MONGO_ROOT_PASSWORD}
ME_CONFIG_MONGODB_SERVER=mongodb
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_OPTIONS_AUTH_SOURCE=admin
ME_CONFIG_BASICAUTH_USERNAME=example
ME_CONFIG_BASICAUTH_PASSWORD=1234567890
```

## Demo

If the bot is running, you can try it out by sending a message to
[@agromant_bot](https://t.me/agromant_bot)

![Demo video](/assets/demo.mp4)
