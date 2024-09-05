import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
import pyperclip
from aiogram.utils.markdown import hlink
import sqlite_db
import asyncio
import aioschedule


botkart = FSInputFile("бот.png")
TOKEN = "6923533328:AAGzGN8a9SidZO5f0RsOZleEzyzTtS5H2iY"
dp = Dispatcher()
promo = "MSKPOTOLKI"
bot = Bot(token=TOKEN, parse_mode='HTML')
ID = -1002090528693
TEXT = "Привет! Для полноценного знакомства с нами и получения бонуса воспользуйтесь нашим ботом"

builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text="Скопировать", callback_data="copy"))

bot_kb = InlineKeyboardBuilder()
bot_kb.row(types.InlineKeyboardButton(text="Перейти", url="https://t.me/ecoceilings_bot"))


menu = InlineKeyboardBuilder()
menu.row(types.InlineKeyboardButton(text="Акции", callback_data="stocks"))
menu.row(types.InlineKeyboardButton(text="О нас", callback_data="about"))
menu.row(types.InlineKeyboardButton(text="Этапы", callback_data="steps"))
menu.row(types.InlineKeyboardButton(text="Отзывы", callback_data="reviews"))
menu.row(types.InlineKeyboardButton(text="Наш сайт", url="https://www.ecopotolki-mos.ru/"))


back_button = types.InlineKeyboardButton(text="Назад", callback_data="back")

stocks_menu = InlineKeyboardBuilder()
stocks_menu.row(types.InlineKeyboardButton(text="Подробнее", url="https://www.ecopotolki-mos.ru/"))
stocks_menu.row(back_button)


about_menu = InlineKeyboardBuilder()
about_menu.row(types.InlineKeyboardButton(text="Почему мы?", url="https://www.ecopotolki-mos.ru/#about"))
about_menu.row(back_button)


back_keyboard = InlineKeyboardBuilder()
back_keyboard.add(back_button)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if await sqlite_db.sql_read(message.from_user.id):
        await message.answer(text="О чем еще Вы хотите узнать?\nНам еще есть чем Вас удивить :)",
                             reply_markup=menu.as_markup())
    else:
        await sqlite_db.sql_add_command(message.from_user.id)
        photo_file = FSInputFile("start.png")
        await message.answer_photo(photo=photo_file,
                                   caption=f"<b>Время скидок</b>🎉🎉\nТак как Вы являетесь новым пользователем, мы дарим Вам скидку на заказ!",
                                   parse_mode='HTML', reply_markup=builder.as_markup())
        await message.answer(text="О чем еще Вы хотите узнать?\nНам еще есть чем Вас удивить :)",
                             reply_markup=menu.as_markup())


@dp.callback_query(F.data == "copy")
async def menu_command(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text="Ваш промокод: MSKPOTOLKI\nНе забудьте скопировать его!")
    await callback.answer(text="")


@dp.callback_query(F.data == "stocks")
async def stocks_command(callback: types.CallbackQuery):
    await callback.answer(text="")
    # await callback.message.answer(text="<b>Скидка 20%</b>🎉🎉\n- При заказе потолков на всю квартиру или дом!"
    #                                    "\n- При заказе нашего освещения! (люстры, светильники, треки и остальное оборудование)"
    #                                    "\n<b>Подробнее на нашем сайте</b>\n👇👇👇👇👇👇👇👇👇👇👇👇👇", reply_markup=stocks_menu.as_markup())
    await callback.message.answer_photo(botkart, caption="<b>Скидка 20%</b>🎉🎉\n- При заказе потолков на всю квартиру или дом!"
                                       "\n- При заказе нашего освещения! (люстры, светильники, треки и остальное оборудование)"
                                       "\n<b>Подробнее на нашем сайте</b>\n👇👇👇👇👇👇👇👇👇👇👇👇👇", parse_mode='HTML', reply_markup=stocks_menu.as_markup())


@dp.callback_query(F.data == "about")
async def about_command(callback: types.CallbackQuery):
    await callback.answer(text="")
    await callback.message.answer(text="Задумывались о натяжных потолках, но сомневайтесь в качестве? Мы поможем вам принять правильное решение!\n\n"
                                       "Более чем 10 лет мы занимаемся установкой натяжных потолков в Москве и Московской области. Выполняем работы "
                                       "по установке натяжных потолков как в жилых помещениях, так и для хозяйственных объектов, вроде студий и офисов.\n\n"
                                       "Мы сотрудничаем с индивидуальными заказчиками и корпоративными клиентами, предлагая тесное партнёрство на всевозможных стадиях проекта - от "
                                       "обговаривания вашего проекта до выезда на объект для замеров, расчета цене и осуществления работ.\n\n"
                                       "Все материалы, с которыми мы работаем, прошли сертификацию в Российской федерации, что помогает нам гарантировать профессионализм в подходе и "
                                       "суровое соблюдение всевозможных условий договора, в том числе стоимость работ, сроки и гарантийные обязательства.",
                                  reply_markup=about_menu.as_markup())


@dp.callback_query(F.data == "steps")
async def steps_command(callback: types.CallbackQuery):
    await callback.answer(text="", parse_mode='HTML')
    await callback.message.answer(text="<b>Как происходит установка натяжных потолков?</b>\n\n"
                                       "Наш замерщик приезжает на объект для точного оценки величин здания, что нужно для корректного расчета материалов и стоимости работы. "
                                       "Расходуя профессиональные инструменты, специалист осуществляет замеры и фиксирует все нюансы здания, в том числе высоту, площадь, и нюансы конструкции.\n\n"
                                       "Далее осуществляется отбивка показателя. С помощью лазерного показателя на стенах здания отмечаются горизонтальные линии, "
                                       "которые станут служить ориентирами для установки профилей натяжного потолка."
                                       "Это значимый этап, так как от верности отбивки показателя находится в зависимости итоговое уровень качества который установлен потолка...\n\n"
                                       "<b>Подробнее на нашем сайте</b>\n👇👇👇👇👇👇👇👇👇👇👇👇👇",
                                  reply_markup=stocks_menu.as_markup())


@dp.callback_query(F.data == "reviews")
async def reviews_command(callback: types.CallbackQuery):
    link = hlink('Ссылка', 'https://yandex.ru/profile/134835560725/')
    await callback.answer(text="")
    await callback.message.answer(text=f"Наши отзывы Вы можете посмотреть на Яндекс картах по ссылке ниже👇👇👇\n\n{link}", reply_markup=back_keyboard.as_markup(), parse_mode='HTML')


@dp.callback_query(F.data == "back")
async def back_command(callback: types.CallbackQuery):
    await callback.answer(text="")
    await callback.message.answer(text="О чем еще Вы хотите узнать?\nНам еще есть чем Вас удивить :)", reply_markup=menu.as_markup())


async def auto_message_command():
    photo_file = FSInputFile("photo_2023-12-10_18-31-43.jpg")
    await bot.send_photo(chat_id=ID, photo=photo_file, caption="Привет! Для полноценного знакомства с нами и получения приятного бонуса воспользуйтесь нашим ботом", reply_markup=bot_kb.as_markup())


async def scheduler():
    aioschedule.every(2).weeks.do(asyncio.run, auto_message_command())
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    await sqlite_db.sql_start()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
