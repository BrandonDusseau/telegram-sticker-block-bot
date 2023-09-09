# Telegram Sticker Block Bot
A Telegram bot to block sticker packs in group chats.

## How it Works
Whenever the bot sees a sticker from a pack that has been banned, it will delete the sticker and display a message to the user that originally sent it.


## Prerequisites
To set up this bot, the following is required:

* A bot token issued by Telegram's BotFather ([documentation](https://core.telegram.org/bots#how-do-i-create-a-bot))
* Docker _or_ Python 3.11 or higher
    * `venv` module is required if using Python without Docker (`python -m pip install venv`)


## Configuration
1. Rename `config.example.json` to `config.json`.
2. Edit `config.json`, setting `owner` to your Telegram **username**, and `token` to your bot token (see _Prerequisites_ above).


## Running the Bot
Once configured, running the bot is simple. Choose the appropriate set of instructions for your installation method.

Both methods require some familiarity with a command-line interface (whether it be a Linux/Unix shell, Command Prompt, or PowerShell).

### Docker (Recommended)
1. Navigate to the bot's root directory.
2. If updating or running the bot for the first time, run `docker-compose build`.
3. Run `docker-compose up -d`.
    1. The `-d` flag is optional, but will allow the container to run in the background.
    2. To stop the bot, run `docker-compose down`. If you started it _without_ the `-d` flag, you will need to abort the program by pressing Ctrl-C first.

### Running Python Directly
_*Note:* Depending on your system you may need to use the `python3` command instead of `python`._

1. Navigate to the bot's root directory.
2. If running the bot for the first time, run `python -m venv env` to create the virtual environment directory.
    1. Using a virtual environment is necessary to avoid polluting your system's Python environment, but you can skip if it you really want to.
3. Activate the virtual environment using [the appropriate command for your system](https://docs.python.org/3/library/venv.html#how-venvs-work).
4. Install the required Python packages (`python -m pip install -r requirements.txt`).
5. Launch the bot with (`python -m stickerblockbot`).
    1. If you want to run the bot in the background, consider using `screen` or `tmux` (or Windows equivalent).


## Using the Bot
Once the bot is running, if everything was set up correctly, you can start using it in Telegram.

First, open a direct message with the bot and send `/start`. The bot will display available commands. I recommend setting up additional bot admins at this point if you so desire.

Once the bot is set up, you can invite it to a Telegram group. The bot MUST be promoted to an administrator in your group to work properly. The only permission it needs is "Delete Messages".


## License
This software is open source under the MIT License. See the `LICENSE.md` file for details on what this means.
