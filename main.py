import os
from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
import random

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

rock_button = InlineKeyboardButton(text= "Камень", callback_data= "rock_callback")
paper_button = InlineKeyboardButton(text= "Бумага", callback_data= "paper_callback")
scissior_button = InlineKeyboardButton(text= "Ножницы", callback_data= "scissior_callback")

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[rock_button],
                     [paper_button],
                     [scissior_button]]
)

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Давай поиграем с тобой в камень/ножницы/бумага',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'rock_callback')
async def rock_callback_proccess(callback: CallbackQuery):
    result = get_result(1)
    print(result)
    await callback.message.answer(
        text=result
    )
    await callback.message.answer(
        text='Еще раз?',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'paper_callback')
async def paper_callback_proccess(callback: CallbackQuery):
    result = get_result(2)
    await callback.message.answer(
        text=result
    )
    await callback.message.answer(
        text='Еще раз?',
        reply_markup=keyboard
    )

@dp.callback_query(F.data == 'scissior_callback')
async def scissior_callback_proccess(callback: CallbackQuery):
    result = get_result(3)
    await callback.message.answer(
        text=result
    )
    await callback.message.answer(
        text='Еще раз?',
        reply_markup=keyboard
    )

def get_result(player_hand):
    bot_hand = random.randint(1,3)
    if player_hand == bot_hand:
        return "Ничья!"
    match bot_hand:
        case 1: #Камень
            return "Вы выиграли! Бумага бьет камень" if player_hand == 2 else "Вы проиграли! Камень бьет ножницы"
        case 2: #Бумага
            return "Вы выиграли! Ножницы режут бумагу" if player_hand == 3 else "Вы проиграли! Бумага бьет камень"
        case 3: #Ножницы
            return "Вы выиграли! Камень бьет ножницы" if player_hand == 1 else "Вы проиграли! Ножницы режут бумагу"
    return player_hand

if __name__ == '__main__':
    dp.run_polling(bot)