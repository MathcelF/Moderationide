import discord
import datetime


# Should also be obvious

class Embed:
    @staticmethod
    def plain(description='description', title='Moderationide — Bot', colour=0x0099FF):
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour(colour),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text='- Moderationide')
        return embed

    @staticmethod
    def info(description, title='Info', colour=0xFAA719):
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour(colour),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text='- Moderationide')
        return embed

    @staticmethod
    def warn(description):
        embed = discord.Embed(
            title='Warning',
            description=description,
            colour=discord.Colour(0xFAA719),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text='- Moderationide')
        return embed

    @staticmethod
    def error(description, title='Error'):
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour(0xCC0000),
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text='- Moderationide')
        return embed

    @staticmethod
    def user_information(colour, hex_set, flag_set, user, author, banned):
        description = '**<@{}>**'.format(user.id)
        embed = discord.Embed(
            title='User Information',
            description=description,
            colour=discord.Colour(int(colour, base=16))
        )
        embed.add_field(name='m_flag [0x{}]'.format(hex_set[0]), value=flag_set[0], inline=False)
        embed.add_field(name='s_flag [0x{}]'.format(hex_set[1]), value=flag_set[1], inline=False)
        embed.add_field(name='Banned:', value=banned)
        embed.set_author(name=author.name, icon_url=author.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text='AuthorID: {} | - Moderationide'.format(author.id))
        return embed

    @staticmethod
    def imperator_information(user, author):
        description = '**<@{}>; You shall not bother the Imperator.**'.format(user.id)
        embed = discord.Embed(
            title='The Imperator',
            description=description,
            colour=discord.Colour(0xFFFFFF)
        )
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text='AuthorID: {} | - Moderationide'.format(author.id))
        return embed

    @staticmethod
    def logging_embed(title, description, user):
        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour(0x26ce89)
        )
        embed.set_author(name=user, icon_url=user.avatar)
        embed.set_footer(text='AuthorID: {} | - Moderationide'.format(user.id))
        return embed
