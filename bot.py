import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**@FarzTagBot**,  ★\nDaha Çox Məlumat üçün  **/komek**'e Basın.",
                    buttons=(
                      [Button.url('🌟 Məni Əlavə Et', 'https://t.me/FarzTagBot?startgroup=a'),
                      Button.url('📣 Kanalımız', 'https://t.me/FarzBotSs'),
                      Button.url('🚀 Support', 'https://t.me/FarzBotSupport')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/komek$"))
async def help(event):
  helptext = "**@FarzTagBot Kömək**\n\nKomut: /cancel\n Bu Komutu İşlədərək Tag Etməyi Dayandıra Bilərsiz.\nKomut: /all \n  Bu Komutu Tag ı Başlatmaq üçün İstifadə Edə Bilərsiz . \n`Məsələn: /all Salam!`"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Məni Əlavə Et', 'https://t.me/FarzTagBot?startgroup=a'),
                       Button.url('📣 Kanalımız', 'https://t.me/FarzBotSs'),
                      Button.url('🚀 Support', 'https://t.me/FarzBotSupport')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Yalnız Gruplarda İşlədilir.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__ Yalnız İdarəçilər İşlədə Bilər!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem! (gruba eklemeden önce gönderilen mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Bana bir argüman ver!__")
  else:
    return await event.respond("__Komutun Yanında Mesaj Olmalıdır!__")
  
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Bot Tag Eləməyi Dayandırdı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Bot Tag Eləməyi Dayandırdı ❌")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot çalıyor merak etme 🚀 @RobotRoomChat bilgi alabilirsin <<")
client.run_until_disconnected()
