from discord.ext import commands
import discord
import configparser

import db

bot = commands.Bot(command_prefix="!")


thisToken = "???"


@ bot.event
async def on_ready():
    print("Discord", "Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@ bot.event
async def on_message(mes: discord.message.Message):
    if mes.author.id == bot.user.id:
        return

    #! HARD CODE
    if mes.channel.id == 895323127268122654:
        studentCode = ""
        content = mes.content.strip()
        #!Don't forget to change
        nickName = ""
        for c in content:
            if len(studentCode) < 10:
                if c in "0123456789":
                    studentCode += c
            else:
                nickName += c
        nickName = nickName.strip()
        nickName = nickName.split()[0]
        print(nickName)
        studentCode = studentCode[:9] + "-" + studentCode[-1]
        if studentCode[2:6] != "3040" and len(studentCode) < 10:
            await mes.author.send(f":x:รหัสนักศึกษา `{studentCode}` ไม่ถูกต้อง\nกรุณาตรวจสอบแล้วลองพิมพ์ใน #verify ใหม่")
            return
        
        if studentCode[0:2] != "63":
            await mes.author.send(f":x: อนุญาตเฉพาะนักศึกษาชั้นปีที่ 2 (รหัส 63) เท่านั้น")
            return

        res = db.getDataOfStuCode(studentCode)

        if not res:
            await mes.author.send(f":x:ไม่พบรหัสนักศึกษา `{studentCode}`\nกรุณาตรวจสอบแล้วลองพิมพ์ใน #verify ใหม่")
            return
        # [(988, '633040158-0', 'นายธนพนธ์ บุญประกอบ', 'CoE', None
        if nickName:
            name = nickName
        else:
            name = res[0][2]
            if name.startswith("นางสาว"):
                name = name[6:]
            elif name.startswith("นาย") or name.startswith("นาง"):
                name = name[3:]
            print(name)
            name = name.split()[0]

        major = res[0][3]

        if studentCode[:2] == "64":
            thisRole = discord.utils.get(mes.guild.roles, name="Freshy")
            await mes.author.edit(nick=f"{name} {major}")
        else:
            thisRole = discord.utils.get(mes.guild.roles, name="Sophomore")
            await mes.author.edit(nick=f".พี่{name} {major}")

        db.requestAttend(mes.author.id, studentCode)

        thatUser = await mes.guild.fetch_member(db.getDiscordIdFromStuCode(studentCode))
        await thatUser.edit(roles=[thisRole])


def runBot():
    print("Reading config...")
    thisConfig = configparser.ConfigParser()
    thisConfig.read("BigConfig.ini")
    thisToken = thisConfig["bot"]["TOKEN"].strip()

    print("Connect to SQL")
    db.connect(thisConfig)

    print("Starting bot...")
    try:
        bot.run(thisToken)
    except Exception as e:
        print(
            "Discord", f"Wrong Token or Fucked up\nhere is token:{thisToken}")
        print(e)
        exit(1)
