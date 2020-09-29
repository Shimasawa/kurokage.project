from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ.get('DISCODE_BOT_TOKEN')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('おはよう')
#展開
@bot.event
async def expand(message):
    url_discord_message = (
        'https://discordapp.com/channels/'
        r'(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
    )
    for ID in re.finditer(url_discord_message, message.content):
        embed = await fetch_embed(ID, message.guild)
        await message.channel.send(embed=embed)


async def fetch_embed(ID, guild):
    if guild.id == int(ID['guild']):
        channel = guild.get_channel(int(ID['channel']))
        message = await channel.fetch_message(int(ID['message']))
        return compose_embed(message)
    else:
        return Embed(title='404')


def compose_embed(message):
    embed = Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed


bot.run(token)
