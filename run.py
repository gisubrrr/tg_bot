from bot_settings import bot
from handlers import welcome, rndm


git init
welcome.register_welcome_handlers()



bot.polling(none_stop=True)