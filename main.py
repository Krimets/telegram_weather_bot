import json
import requests
import config
import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    if 'погода' in message.text.lower():
        text = message.text.split()
        for _ in text:
            _ = _.replace(',', '').replace('.', '').replace(':', '').replace(';', '').replace('"', '').replace("'", '')
            if _.lower() != 'погода':
                await message.answer(await get_weather_func(_))


async def get_weather_func(text):
    response_get_weather = requests.get(config.weather_api.format(city=text))
    if response_get_weather.status_code != 200:
        return 'Вибач, але такого міста я не знаю :('
    else:
        data = json.loads(response_get_weather.content)
        print(data)
        temp = round(data['main']['temp'] - 273.15)
        feels_like = round(data['main']['feels_like'] - 273.15)
        mess = presentation(temp, feels_like, text)
        return mess


def presentation(temp, feels_like, text):
    return f'{text}\nЗараз температура {temp} градусів\nВідчувається як {feels_like}'


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)