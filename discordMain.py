from discord.ext import commands
import discord
import configparser
import RandomGroup as rg
import anotherData as ad

import db

bot = commands.Bot(command_prefix="!")


thisToken = "???"


@ bot.event
async def on_ready():
    print("Discord", "Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')


def getCategory(tarnInd, guild):
    thatList = guild.categories
    thatCataId = ad.getCataId(tarnInd)
    for e in thatList:
        if e.id == thatCataId:
            thatGuild = e
            break

    return thatGuild


async def setCategoryGroup(tarnInd, Group, guild):
    thatCate = getCategory(tarnInd, guild)
    ad.addNewGroupOfCategory(tarnInd, Group)
    seeRole = discord.utils.get(guild.roles, name=f"Group {Group}")
    await thatCate.set_permissions(seeRole,
                                   view_channel=True,
                                   )


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

    if mes.channel.id == 857939411743670283:
        #!Danger zone
        content = mes.content.strip() or ""

        if content.lower().startswith("!assigngroup"):
            await mes.channel.send(":game_die:กำลังจัดกลุ่มน้อง ๆ ")
            resultGroup = rg.groupAssignAll()
            freshRole = discord.utils.get(mes.guild.roles, name="Freshy")
            for groupInd, members in enumerate(resultGroup):
                print(f"Adding role Group {groupInd+1}...")
                thisRole = discord.utils.get(
                    mes.guild.roles, name=f"Group {groupInd+1}")
                for mem in members:
                    try:
                        thatUser = await mes.guild.fetch_member(int(mem))
                        await thatUser.edit(roles=[freshRole, thisRole])
                    except:
                        print(
                            f"Warning... {mem}({db.getStuCodeFromDiscordId(mem)}) is missing!")
            await mes.channel.send(":game_die:สำเร็จแล้ว")

        elif content.lower().startswith("!test"):
            await mes.channel.send(":apple:ว่าไง")
        elif content.lower().startswith("!reset"):

            await mes.channel.send(f":gear:กำลัง Reset")

            for i in range(10):
                pp = ad.getPrevGroupOfCategory(i+1)
                thatCate = getCategory(i+1, mes.guild)
                for e in pp:
                    notSeeRole = discord.utils.get(
                        mes.guild.roles, name=f"Group {e}")
                    await thatCate.set_permissions(notSeeRole,
                                                   view_channel=False,
                                                   )
                ad.resetPrevGroupOfCategory(i+1)

            await mes.channel.send(f":sunglasses: **ปิดการมองเห็น!!!!!**")

        elif content.lower().startswith("!forcereset"):
            await mes.channel.send(f":gear:กำลัง force Reset")
            for i in range(10):
                print(f"Closing {i+1}")
                for j in range(rg.N_GROUP):
                    print(f"({j+1}/{rg.N_GROUP})")
                    thatCate = getCategory(i+1, mes.guild)
                    notSeeRole = discord.utils.get(
                        mes.guild.roles, name=f"Group {j+1}")
                    await thatCate.set_permissions(notSeeRole,
                                                   view_channel=False,
                                                   )
            await mes.channel.send(f":sunglasses: **ปิดการมองเห็น!!!!!**")

        elif content.lower().startswith("!nextgame"):
            await mes.channel.send(f":gear:กำลัง เปลี่ยนผลัด...")
            newInd = content.lower().replace("!nextgame", "").strip()
            if not newInd:
                await mes.channel.send(":warning: กรุณาใส่เลขผลัด (ใส่เป็น 1-5)")
                return
            try:
                int(newInd)
            except:
                await mes.channel.send(":warning: กรุณาใส่เลขผลัดวันนี้เป็นจำนวนเต็ม (ใส่เป็น 1-5)")
                return

            newInd = int(newInd)

            if newInd > 5 or newInd < 1:
                await mes.channel.send(":warning: กรุณาใส่เลขผลัด 1 ถึง 5")
                return

            ad.setNowIndGame(newInd)

            for i in range(10):
                pp = ad.getPrevGroupOfCategory(i+1)
                thatCate = getCategory(i+1, mes.guild)
                for e in pp:
                    notSeeRole = discord.utils.get(
                        mes.guild.roles, name=f"Group {e}")
                    await thatCate.set_permissions(notSeeRole,
                                                   view_channel=False,
                                                   )
                ad.resetPrevGroupOfCategory(i+1)

            for i in range(rg.N_GROUP):
                newTarn = ad.getTarnOfGroup(i+1, newInd)
                await setCategoryGroup(newTarn, i+1, mes.guild)
            await mes.channel.send(f":video_game: **เริ่มผลัดที่ `{newInd}` !!!!!**")


def runBot():
    print("Reading config...")
    thisConfig = configparser.ConfigParser()
    thisConfig.read("BigConfig.ini")
    thisToken = thisConfig["bot"]["TOKEN"].strip()

    print("Connect to SQL")
    db.connect(thisConfig)

    print("Loading data...")
    ad.loadData()

    print("Starting bot...")
    try:
        bot.run(thisToken)
    except Exception as e:
        print(
            "Discord", f"Wrong Token or Fucked up\nhere is token:{thisToken}")
        print(e)
        exit(1)
