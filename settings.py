import datetime
import random

GROUP_ID = 194086943
TOKEN = ''

INTENTS = [
    {
        "name": "Купить билет",
        "tokens": ("/ticket", "поехали", "Поехали", "купить", "Купить", "билет", "Билет", "полетели", "Полетели"),
        "scenario": "/ticket",
        "answer": None
    },
    {
        "name": "Справка",
        "tokens": ("/help", "помощь", "Помощь", "справка", "Справка", "информация", "Информация", "функции", "Функции",
                   "привет бот", "Привет бот", "привет", "Привет",),
        "scenario": None,
        "answer": "Бот предназначен для заказа авиабилетов на самолет. Команды для заказа билета: \n "
                  "'/ticket'\n'поехали'\n'купить'\n'билет'\n'полетели'\n"
    },
]

SCENARIO = {
    "/ticket": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Откуда летим?",
                "failure_text": "Из этого города нет рейсов. Вот варанты городов, откуда возможен перелёт:",
                "handler": "dispatcher_city_departure",
                "next_step": "step2"
            },
            "step2": {
                "text": "Куда летим?",
                "failure_text": "В этот город нет рейсов. Вот варанты городов, куда возможен перелёт",
                "handler": "dispatcher_city_arrival",
                "next_step": "step3"
            },
            "step3": {
                "text": "Когда? (введите дату в формате: ДД-ММ-ГГГГ)",
                "failure_text": "Неверный формат даты (введите дату в формате: ДД-ММ-ГГГГ)",
                "handler": "dispatcher_date",
                "next_step": "step4"
            },
            "step4": {
                "text": " ",
                "failure_text": "Нет такого рейса (введите номер)",
                "handler": "dispatcher_route",
                "handler1": "dispatcher_flight",
                "next_step": "step5"
            },
            "step5": {
                "text": "Сколько нужно мест? (от 1 до 5)",
                "failure_text": "Возможен заказ максимум 5 билетов",
                "handler": "dispatcher_number",
                "next_step": "step6"
            },
            "step6": {
                "text": "Комментарий (ваши пожелания)",
                "failure_text": None,
                "handler": "some_text",
                "next_step": "step7"
            },
            "step7": {
                "text": "Подтвердите правильность введённых данных (да/нет)",
                "failure_text": "Введите 'да', если данные верны или 'нет', если хотя бы одно поле неверно",
                "handler": "yes_or_not",
                "handler1": "confirmation_entered_data",
                "next_step": "step8"
            },
            "step8": {
                "text": "Введите ваш номер телефона для связи",
                "failure_text": "Видимо вы указываете не номер телефона. Повторите попытку",
                "handler": "phone",
                "next_step": "step9"
            },
            "step9": {
                "text": "Спасибо за заказ",
                "failure_text": None,
                "handler": None,
                "next_step": None
                  }
        }
    }
}
DEFAULT_ANSWER = "Не знаю такой команды. Могу помочь с заказом билета на самолё\n Чтобы получить справку введите: \n" \
                 "'/help'\n'помощь'\n'справка'\n'информация'\n'функции'\n'привет бот'\n'привет'"
