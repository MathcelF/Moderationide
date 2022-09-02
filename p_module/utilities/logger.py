import logging
import logging.config

logging.basicConfig(filename='logs/bot.log',
                    filemode='a',
                    format='[%(asctime)s%(msecs)03dZ] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S.',
                    level=0)

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})


# Creates a custom Level, e.g [WARN] exists in logging, while [COMMAND] does not exist.
# So we create our own Level e.g. [COMMAND] for our purposes.

class CreateLevel:
    def create_command_level(self):
        logging.log(1, self)

    def create_action_level(self):
        logging.log(2, self)


logging.addLevelName(1, 'COMMAND')
logging.addLevelName(2, 'ACTION')
logging.command = CreateLevel.create_command_level
logging.action = CreateLevel.create_action_level
logging.Logger.command = CreateLevel.create_command_level
logging.Logger.action = CreateLevel.create_action_level


class Log:
    @staticmethod
    def action(text):
        logging.action(text)

    @staticmethod
    def command(text):
        logging.command(text)

    @staticmethod
    def info(text):
        logging.info(text)

    @staticmethod
    def warn(text):
        logging.warning(text)

    @staticmethod
    def error(text):
        logging.error(text)

    @staticmethod
    def critical(text):
        logging.critical(text)
