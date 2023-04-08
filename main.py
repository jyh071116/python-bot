import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

@bot.event
async def on_message(message): #모든 메세지 입력 감지
    if message.author.bot: #봇은 제외
        return
    if (message.channel.id == 921011604265504781): #특정 채널(일반)에서 보낸 메세지인지 감지
        if message.attachments:
            for attachment in message.attachments: #모든 첨부 파일 확인
                if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif')): #확장자가 이미지 파일이라면
                    image_role = discord.utils.get(message.guild.roles, name='이미지테스트') #image_role 변수에 이미지테스트 역할 정보를 넣음
                    await message.author.add_roles(image_role) #image_role 역할 부여
                    return
    await bot.process_commands(message)
    
@bot.command()
async def roll(ctx, diceCount: int, diceRange: int):
    """
    반복 횟수와 범위를 정해 랜덤으로 주사위를 돌려준다.
    명령어 사용법: /roll 반복횟수 범위
    """
    diceArr = []
    diceSum = 0
    for i in range(diceCount): #diceArr에 랜덤으로 값 추가(주사위 굴리기)
        diceArr.append(random.randrange(1, diceRange+1))
        diceSum += diceArr[i]
        
    diceArrPrint = str(diceArr)[1:-1] #배열을 출력할 때 나오는 대괄호 제거
    embed = discord.Embed(title='주사위',description='명령어 사용법: /roll 반복횟수 범위. 모든 명령어 목록: /help' ,color=0x0aa40f) #주사위를 굴린 결과에 대한 임베드
    embed.add_field(name='각 주사위 결과', value=diceArrPrint, inline=True)
    embed.add_field(name='합', value=diceSum, inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def DeleteRole(ctx):
    """
    특정 역할을 모두 지운다.
    명령어 사용법 /DeleteRole
    """
    admin_role = discord.utils.get(bot.guilds[0].roles, name='admin') #admin_role 변수에 admin 역할 정보를 넣음
    if admin_role in ctx.author.roles: #만약 이 명령어를 입력한 사람이 admin_role이 있다면 명령 실행
        image_role = discord.utils.get(bot.guilds[0].roles, name='이미지테스트') #image_role 변수에 이미지테스트 역할 정보를 넣음
        guild = bot.get_guild(921011604265504778) #길드가 현재 서버를 가르치도록 설정
        
        async for member in guild.fetch_members(limit=150): #모든 멤버를 선택
            await member.remove_roles(image_role) #image_role 역할 삭제


bot.run('MTA5MzkzNjk2OTA2MDQ2NjcxOA.GWfZep.-4xxBCQUQI-62Q_j7rpeeyVGfvCZgochy1QaYY')