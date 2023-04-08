import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

@bot.event
async def on_message(message): #모든 메세지 입력 감지
    if message.author.bot: #봇은 제외
        return
    if (message.channel.id == 1094170937257115759): #특정 채널(일반)에서 보낸 메세지인지 감지
        if message.attachments:
            for attachment in message.attachments: #모든 첨부 파일 확인
                if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif', 'mp4')): #확장자가 이미지 파일이라면
                    image_role = discord.utils.get(message.guild.roles, name='이미지테스트') #image_role 변수에 이미지테스트 역할 정보를 넣음
                    await message.author.add_roles(image_role) #image_role 역할 부여
                    return
                
    if (message.channel.id == 1094170966076174366): #특정 채널(일반)에서 보낸 메세지인지 감지
        if 'd' in message.content: #d가 명령어에 있으면
            diceCase = 0
            diceCount, diceRange = map(str, message.content.split('d')) #d를 기준으로 앞은 diceCount에 대입, 뒤는 diceRange에 대입
            diceCount = int(diceCount)#str이였던 diceCount를 int형으로 변경
            if ' ' in diceRange:
                diceRange, diceStandardValue = map(int, diceRange.split()) #공백을 기준으로 앞은 diceRange에 대입, 뒤는 diceStandardValue를 대입
                diceCase = 2
            elif '+' in diceRange:
                diceRange, diceAfterSum = map(int, diceRange.split('+')) #공백을 기준으로 앞은 diceRange에 대입, 뒤는 diceAfterSum를 대입
                diceCase = 3
            else:
                diceRange = int(diceRange)#str이였던 diceRange를 int형으로 변경
                diceCase = 1
            diceArr = []
            diceSum = 0
            for i in range(diceCount): #diceArr에 랜덤으로 값 추가(주사위 굴리기)
                diceArr.append(random.randrange(1, diceRange+1))
                diceSum += diceArr[i]
            
            if diceCase == 3:
                diceSum += diceAfterSum
                
            diceArrPrint = str(diceArr)[1:-1] #배열을 출력할 때 나오는 대괄호 제거
            embed = discord.Embed(title='',description='' ,color=0x0aa40f) #주사위를 굴린 결과에 대한 임베드
            embed.add_field(name='각 주사위 결과', value=diceArrPrint, inline=True)
            embed.add_field(name='합', value=diceSum, inline=True)
            if diceCount==1 and diceRange==100 and diceCase==2:
                if diceSum == 1:
                    embed.add_field(name='대성공', value='', inline=False)
                elif diceSum<=(diceStandardValue/5):
                    embed.add_field(name='극단적 성공', value='', inline=False)
                elif diceSum<=(diceStandardValue/2):
                    embed.add_field(name='어려운 성공', value='', inline=False)
                elif diceSum<=diceStandardValue:
                    embed.add_field(name='보통 성공', value='', inline=False)
                elif (diceSum == 100) or (diceStandardValue<=50 and diceSum>=96):
                    embed.add_field(name='대실패', value='', inline=False)
                elif diceSum>diceStandardValue:
                    embed.add_field(name='실패', value='', inline=False)
            await message.channel.send(embed=embed)
            
    await bot.process_commands(message)

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
        
        async for member in guild.fetch_members(limit=100): #모든 멤버를 선택
            await member.remove_roles(image_role) #image_role 역할 삭제


bot.run('###')