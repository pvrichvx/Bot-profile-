import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

PROFILE_CHANNEL_ID = 1381277483554574457  
PRIVATE_CHANNEL_ID = 1381568733365010605  

# 🛡️ กันการใช้คำสั่งซ้ำพร้อมกัน
in_progress = set()

@bot.event
async def on_ready():
    print(f'✅ Bot พร้อมใช้งานในชื่อ: {bot.user}')

@bot.command()
async def pf(ctx):
    if ctx.channel.id != PRIVATE_CHANNEL_ID:
        return await ctx.send("❌ ใช้คำสั่งนี้ในห้องที่กำหนดเท่านั้นค่ะ")

    if ctx.author.id in in_progress:
        return await ctx.send("⏳ มีผู้ใช้กำลังสร้างโปรไฟล์อยู่ รอสักครู่ก่อนนะคะ")

    in_progress.add(ctx.author.id)
    try:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        questions = [
            "ขอเลขประจำตัวค่ะ",
            "ชื่อเล่น",
            "ชื่อในเกม",
            "ชื่อเฟส",
            "ขอโปรไฟล์เกมหน่อยค่ะ [ส่งเป็นรูปภาพ]"
        ]

        answers = []

        for i, question in enumerate(questions):
            msg = await ctx.send(question)
            try:
                reply = await bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await msg.edit(content="❌ หมดเวลาในการตอบ โปรดลองใหม่อีกครั้งค่ะ")
                return
            await msg.delete()
            await reply.delete()

            if i == len(questions) - 1:
                # ถ้าเป็นรูปภาพ
                if not reply.attachments:
                    return await ctx.send("❌ โปรดแนบรูปโปรไฟล์เกมด้วยนะคะ")
                image_file = await reply.attachments[0].to_file()
                answers.append(image_file)
            else:
                answers.append(reply.content)

        # สร้างข้อความโปรไฟล์
        user_mention = ctx.author.mention
        profile_text = f"""╭ ─ ୨୧ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╮
                     <a:whitewing1:1381270108630159460> 𝑷𝑹𝑶𝑭𝑰𝑳𝑬 <a:whitewing2:1381270024315994273> 
      เลขประจำตัว : {answers[0]}
      ชื่อเล่น : {answers[1]}
      ชื่อในเกม : {answers[2]}
      <a:1000009473:1381559143537840150>Facebook : {answers[3]}
      <a:emoji_102:1381560618171109386> Discord : {user_mention}
╰ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ୨୧ ─ ╯"""

        profile_channel = bot.get_channel(PROFILE_CHANNEL_ID)
        await profile_channel.send(profile_text)
        await profile_channel.send(file=answers[-1])  

        await ctx.send(f"✅ สร้างโปรไฟล์สำเร็จ {user_mention}")
    
    finally:
        in_progress.remove(ctx.author.id)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)