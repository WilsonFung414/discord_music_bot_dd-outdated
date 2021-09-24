import discord
from discord.ext import commands
import os

# TOKEN = 'ODY1Njc3MDM3NTg1NTYzNjU4.YPHekQ.LaEHW7mBZq73rCZ90SPN27zMwfw' #Test bot
TOKEN = 'ODY0MTE4MzU0MTA0NjgwNDQ4.YOwy7g.snxEWVUz0gP_Y04xKyjbtn2xT7c'
prefix = "."
intents = discord.Intents.all()
intents.members = True

class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        name = dict()
        cogs_list = []
        embed=discord.Embed(title="", description="Run a command by typing the prefix`.`\nI will disconnect when there is nobody in the voice channel.", color=0x71368a)
        embed.set_author(name="Bot Help", icon_url="https://cdn.discordapp.com/attachments/864796912431529984/864800008926658570/zU72OLZ-removebg-preview.png")
        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/864796912431529984/864799136410501120/ZZfsqPE-removebg-preview.png?width=514&height=468")
        embed.set_footer(text="WAH")
        for cogs in mapping:
            if(cogs==None):
                break;
            name[cogs.qualified_name] = [command.name for command in mapping[cogs]]
        for variable in name:
            cmdstr = ""
            for cmd in name.get(variable):
                cmdstr += '`'+cmd + '` '
            embed.add_field(name=variable, value=cmdstr)
        await self.get_destination().send(embed=embed)

client = commands.Bot(intents=intents, command_prefix=prefix, help_command=CustomHelpCommand())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=".help"))
    print('We have logged in as {0.user}'.format(client))
    print("---------------------------------------------------")

# @client.event
# async def on_member_join(member):
#     print("join")
if __name__ == "__main__":
    client.run(TOKEN)
