import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='-', intents=intents)

PROFILE_CHANNEL_ID = 1381277483554574457  
PRIVATE_CHANNEL_ID = 1381568733365010605  

# 🛡️ ป้องกันการใช้งานพร้อมกันหลายคน
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
        sent_msgs = []

        for i, question in enumerate(questions):
            msg = await ctx.send(question)
            sent_msgs.append(msg)
            try:
                reply = await bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await msg.edit(content="❌ หมดเวลาในการตอบ โปรดลองใหม่อีกครั้งค่ะ")
                return
            answers.append(reply)

        # ตรวจสอบรูปภาพคำตอบสุดท้าย
        if not answers[-1].attachments:
            await ctx.send("❌ โปรดแนบรูปโปรไฟล์เกมด้วยนะคะ")
            return
        image_file = await answers[-1].attachments[0].to_file()

        # สร้างข้อความโปรไฟล์
        user_mention = ctx.author.mention
        profile_text = f"""╭ ─ ୨୧ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╮
                     <a:whitewing1:1381270108630159460> 𝑷𝑹𝑶𝑭𝑰𝑳𝑬 <a:whitewing2:1381270024315994273> 
      เลขประจำตัว : {answers[0].content}
      ชื่อเล่น : {answers[1].content}
      ชื่อในเกม : {answers[2].content}
      <a:1000009473:1381559143537840150>Facebook : {answers[3].content}
      <a:emoji_102:1381560618171109386> Discord : {user_mention}
╰ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ୨୧ ─ ╯"""

        profile_channel = bot.get_channel(PROFILE_CHANNEL_ID)
        if profile_channel is None:
            await ctx.send("❌ ไม่พบช่องโปรไฟล์ โปรดตรวจสอบ PROFILE_CHANNEL_ID ค่ะ")
            return

        await profile_channel.send(profile_text)
        await profile_channel.send(file=image_file)

        # 🔻 ลบข้อความที่ถาม & ตอบทั้งหมด (รวมรูป)
        for msg in sent_msgs:
            await msg.delete()
        for reply in answers:
            await reply.delete()

        await ctx.send(f"✅ สร้างโปรไฟล์สำเร็จ {user_mention}")

    finally:
        in_progress.remove(ctx.author.id)

# 🔐 ใช้ Token จากตัวแปรแวดล้อม หรือจะใส่ตรงนี้ก็ได้ (ถ้าทดสอบ)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)