import asyncio


from aiogram import Bot, Dispatcher, types, executor

from config import config, token
from message import MESSAGE_PRICE


loop = asyncio.get_event_loop()

bot = Bot(token['TOKEN'],parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot,loop=loop)

PRICE = types.LabeledPrice(label='Телефон',amount=240000)

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    await m.reply(MESSAGE_PRICE['price'],reply=False)

@dp.message_handler(commands=['buy'])
async def buy(m: types.Message):
    if config['provaider_token'].split(':')[1] == 'TEST':
        await bot.send_message(m.chat.id,'ТЕСТОВОЕ ОПЛАЧЕВОНИЕ')
    
    await bot.send_invoice(
        m.chat.id,
        title=config['title'],
        description=config['description'],
        provider_token=config['provaider_token'],
        currency=config['currency'],
        photo_url=config['photo_url'],
        photo_height=940,  
        photo_width=1112,
        photo_size=940,
        is_flexible=False,
        prices=[PRICE],
        start_parameter='phone',
        payload='some-invoice-payload-for-our-internal-use'
    )

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(m: types.Message,pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await m.reply('Тест прошел успешно!')


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)