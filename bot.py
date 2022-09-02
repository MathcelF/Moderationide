import discord
from discord.ext import commands
from os import listdir

from p_modules import get
from p_modules.graphical import msglist
from p_modules.graphical.embeds import Embed
from p_modules.utilities import logger

import cogs.commands.modules.bot as bot_module

bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix="-",
    help_command=None
)

for filename in listdir('./cogs/commands'):
    if filename.endswith('.py'):
        bot.load_extension('cogs.commands.{}'.format(filename[:-3]), store=False)
    logger.Log.action('Cogs loaded successfully')


@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        return None


@bot.event
async def on_ready():
    logger.Log.action('Connection to ({}{}) successful!'.format(bot.user.name, bot.user.discriminator))
    print(msglist.boronide_art)

for filename in listdir('./cogs/events'):
    if filename.endswith('.py'):
        bot.load_extension('cogs.events.{}'.format(filename[:-3]), store=False)
        logger.Log.action('Loaded Cog: {}'.format(filename[:-3]))

try:
    bot.run(get.config('token'))
except Exception as e:
    logger.Log.error('Logging into ModerationideV2 failed: [{}]'.format(e))
