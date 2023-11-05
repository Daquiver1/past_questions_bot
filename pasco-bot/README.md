## Past Questions Bot
A simple past questions telegram bot with a mock database. Got lots of inspiration from [here](https://github.com/Daquiver1/past_questions_bot) and the official documentation [here](https://docs.python-telegram-bot.org/en/v20.6/).

## Description
This telegram bot allows you search through past questions from a list and download your prefered choice.

## Setting Up The Bot
- You will need a bot API key from @botfather on telegram before you clone this app.
- Clone this repository
```bash
git clone "link to my repo"
```
- In the project directory create a .env file to store your token like this
```bash
TOKEN="your-token"
```
#### step 2: Install poetry if you don't have it already

```bash
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -
```

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> _Note: If you have installed Python through the Microsoft Store, replace py with python in the command above._

> _Reference: [Poetry Installation](https://python-poetry.org/docs/#installation)_

#### step 3: Create a virtual environment

```bash
poetry shell
```

#### Step 4: Install dependencies

```
poetry install
```
- Start The Bot
```
python3 bot.py
```

## Commands

| Command   | Description                                  |
|-----------|----------------------------------------------|
| /start    | Start a conversation with the bot.           |
| /search   | Initiate a search for past questions.        |
| /list     | List all available past questions.           |
| /help     | Display a menu of available commands.        |


## Todo
- [ ] Add InlineKeyboard support.
- [ ] Makes file retrieval fast.

I documented some challenges I faced [here](https://docs.google.com/document/d/1977jFNuiUok-bW9EE6tRW9b-SlagDbzJShCk2GnHz0M/edit?usp=sharing).