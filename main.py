@bot.command()
async def pf(ctx):
    if ctx.channel.id != PRIVATE_CHANNEL_ID:
        return await ctx.send("❌ ใช้คำสั่งนี้ในห้องที่กำหนดเท่านั้นนะคะ")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("ขอเลขประจำตัวค่ะ")
    id_msg = await bot.wait_for('message', check=check)
    await id_msg.delete()

    await ctx.send("ชื่อเล่น")
    name_msg = await bot.wait_for('message', check=check)
    await name_msg.delete()

    await ctx.send("ชื่อในเกม")
    ign_msg = await bot.wait_for('message', check=check)
    await ign_msg.delete()

    await ctx.send("ชื่อเฟส")
    fb_msg = await bot.wait_for('message', check=check)
    await fb_msg.delete()

    await ctx.send("ขอโปรไฟล์เกมหน่อยค่ะ [ส่งเป็นรูปภาพ]")
    profile_pic_msg = await bot.wait_for('message', check=check)
    if not profile_pic_msg.attachments:
        return await ctx.send("❌ โปรดแนบรูปโปรไฟล์เกมด้วยนะคะ")
    await profile_pic_msg.delete()

   