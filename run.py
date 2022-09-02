import discord
from discord.ext import commands
from p_modules.graphical import embeds
from p_modules.utilities.piston import PistonAPI
from p_modules.utilities import logger
import re
import os


class Var:
    max_characters = 75
    bot_channel_id = 1001530523790876762


class Run(commands.Cog, name='Runs Code'):

    def __init__(self, bot):
        self.bot = bot
        self.api = PistonAPI()

    @commands.command()
    async def run(self, ctx, *, args: str):
        if ctx.channel.id != Var.bot_channel_id and ctx.guild:
            await ctx.reply(embed=embeds.Embed.warn('Only available in: <#{}>'.format(var.bot_channel_id)))
            return None
        if not (match := re.fullmatch(r'((```)?)([a-zA-Z\d]+)\n(.+?)\1', args, re.DOTALL)):
            await ctx.reply(embed=embeds.Embed.warn('Code is not in a Markdown'))
            return None
        try:
            await self.api.load_environments()
            *_, lang, source = match.groups()

            if not (language := self.api.get_language(lang)):
                await ctx.reply(embed=embeds.Embed.warn('Language: **`{}`** is not supported!'.format(lang)))
                return None

            result = await self.api.run_code(language, source)
            output = result['run']['output']

            if len(output) > Var.max_characters:
                new_line = output.find('\n', Var.max_characters, Var.max_characters + 20)
                if new_line == -1:
                    new_line = Var.max_characters
                output = output[:new_line] + '\n...'

            description = '```\n' + output.replace('`', '`\u200b') + '\n```'
            title = 'Boronide Code-Execution: {}'.format(language)

            if result['run']['code'] != 0:
                error_embed = embeds.Embed.error(title=title, description=description)
                await ctx.reply(embed=error_embed)
                return None

            plain_embed = embeds.Embed.plain(title=title, description=description, colour=0x53A653)
            await ctx.reply(embed=plain_embed)
        except Exception as e:
            logger.Log.error('Exception occurred in {} [{}]'.format(e, os.path.splitext(os.path.basename(__file__))[0]))
            pass


def setup(bot):
    bot.add_cog(Run(bot))
