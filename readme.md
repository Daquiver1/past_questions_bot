# Past Question Telegram Bot

PyBot is a Telegram bot designed to assist users with accessing past question files. It allows users to search for specific past question files, submit queries and suggestions, and receive help with available commands.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/childerx/past_questions_bot
   ```

#### Navigate to the project directory:

```sh
cd botfolder
```

#### Install the required packages:

```sh
pip install -r requirements.txt
```

#### Create a .env file in the project directory with the following content:

```sh
BOT_TOKEN=YOUR_BOT_TOKEN
```

Replace YOUR_BOT_TOKEN with your actual Telegram bot token obtained from BotFather.

# Usage

To run the PyBot Telegram bot, execute the following command in the project directory:

```sh
python main.py
```

# Commands

- **/start**: Initiates the bot and provides a welcome message.
- **/help**: Displays information about available commands.
- **/search**: Allows users to search for specific past question files.
- **/request**: Allows users to submit queries and suggestions.
- **/cancel**: Cancels the ongoing conversation.

# Conversation Flow

## Search Command

Users can type the name of the past question they want to search for. PyBot will fetch any file matching the typed input.

## Request Command

Users can send queries and suggestions to the bot. These inputs will be processed and saved for further actions.

# Error Handling

- If an unknown command is provided, the bot will respond with a message indicating the command is not recognized.
- Error messages related to processing user requests are sent to the specified Telegram user.

# Compatibility

- **Telegram API Version**: This bot example requires `python-telegram-bot` version 20.0.0-alpha5 or higher.

For more information about the Telegram Bot API and how to create your own bot, visit the [official Telegram Bot API Documentation](https://core.telegram.org/bots/api).

## Challenges Faced

- I encountered several challenges while implementing the request command, where users input their requests and the bot saves them to a text file. However, I successfully resolved these issues in the end.
- 
<img width="551" alt="Screenshot 2023-11-05 at 11 51 47 PM" src="https://github.com/childerx/past_questions_bot/assets/102569865/ee360d0e-f400-462d-ba46-0cf315950c7e">

<img width="547" alt="Screenshot 2023-11-05 at 11 53 50 PM" src="https://github.com/childerx/past_questions_bot/assets/102569865/d9edd77c-56c8-48d9-bd6f-7779b43d39ce">

<img width="614" alt="Screenshot 2023-11-05 at 11 55 31 PM" src="https://github.com/childerx/past_questions_bot/assets/102569865/02bb6a05-6625-495b-9aa2-9eda2f425434">



