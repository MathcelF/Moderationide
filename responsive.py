import discord
from discord.commands import slash_command
from discord.ext import commands

from p_modules import get
from p_modules.graphical.embeds import Embed
import cogs.commands.modules.responsive as responsive_module


class Responsive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config('gid'), description='Help with Obfuscation (RU, DE, EN)')
    async def help(self, ctx: commands.Context):
        view = discord.ui.View(timeout=None)

        for language in responsive_module.languages:
            view.add_item(UIButton(language))

        description = '**Click the Button to get a tutorial video in the according language**'
        embed = Embed.plain(description=description, title='Boronide Usage Tutorial')
        await ctx.respond(embed=embed, view=view)

    @slash_command(guild_ids=get.config('gid'), description='Information about the Moderationide Bot')
    async def info(self, ctx: commands.Context):
        title = 'Information: Moderationide V2.0.0'
        description = '**Bot written by <@581513863640514571>\nGitHub: [soon]**'
        embed = Embed.plain(title=title, description=description)
        await ctx.respond(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        view = discord.ui.View(timeout=None)
        for language in responsive_module.languages:
            view.add_item(UIButton(language))

        self.bot.add_view(view)


class UIButton(discord.ui.Button):
    def __init__(self, language):
        super().__init__(label=language, style=discord.enums.ButtonStyle.primary, custom_id=str(language))

    async def callback(self, interaction: discord.Interaction):
        language = interaction.data['custom_id']
        if language not in responsive_module.languages:
            embed = Embed.error(description='Error occurred while fetching your request', title='Error with Command')
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        for c, i in enumerate(responsive_module.languages):
            if language == i:
                return await interaction.response.send_message(responsive_module.video_list[c], ephemeral=True)


def setup(bot):
    bot.add_cog(Responsive(bot))
