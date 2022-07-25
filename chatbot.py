import random
import logging
import dispatcher

try:
    import settings
except ImportError:
    exit('DO cp settings.py.default settings.py and set TOKEN')

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

log = logging.getLogger('bot')


def logging_configurate():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.txt', 'w', encoding='cp1251')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%d-%m-%Y %H:%M'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class UserState:
    """Состояние пользователя внутри сценария"""

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


class Bot:
    """Эхо-бот для Вконтакте
    Use Python 3.7"""

    def __init__(self, group_id, token):
        """
        :param group_id: ID группы ВК
        :param token: секретный token
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
        self.long_pol = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.user_state = dict()  # user_id -> UserState

    def run(self):
        """Запуск бота"""
        for events in self.long_pol.listen():
            try:
                self.on_event(events)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """Обработка соощения бота"""
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Не знаю такого типа события %s', event.type)
            return
        user_id = event.object.message['peer_id']
        text = event.object.message['text']
        if user_id in self.user_state:
            text_to_send = self.continue_scenario(user_id, text=text)
        else:
            for intent in settings.INTENTS:
                if any(token in text for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
                else:
                    text_to_send = settings.DEFAULT_ANSWER

        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def start_scenario(self, user_id, scenario_name):
        # начало сценария
        scenario = settings.SCENARIO[scenario_name]  # словарь "/ticket"
        first_step = scenario['first_step']  # "step1"
        step = scenario['steps'][first_step]  # словарь "step1"
        text_to_send = step['text']  # "Откуда летим"
        self.user_state[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)  # в стейт записывается
        # название scenario_name="/ticket", step_name="step1"
        return text_to_send

    def continue_scenario(self, user_id, text):
        # продолжение сценария
        state = self.user_state[user_id]  # UserState(scenario_name=scenario_name, step_name=first_step)
        step = settings.SCENARIO[state.scenario_name]['steps'][state.step_name]  # словарь "step1"
        handler = getattr(dispatcher, step['handler'])  # из модуля dispatcher получается функция
        # dispatcher_city_departure
        next_step = settings.SCENARIO[state.scenario_name]['steps'][step['next_step']]  # "step2"
        print(state.context)
        if handler(text=text, context=state.context) and next_step['text'] == " ":
            # следующий шаг
            handler = getattr(dispatcher, next_step['handler1'])
            text_to_send = handler(text=text, context=state.context)
            if next_step['next_step']:  # если у "step2" есть "next_step"
                state.step_name = step['next_step']  # то в стейт записывается step_name="step2"
            else:
                self.user_state.pop(user_id)
        elif next_step['text'] == "Подтвердите правильность введённых данных (да/нет)":
            handler = getattr(dispatcher, next_step['handler1'])
            text_to_send = handler(text=text, context=state.context)
            if handler(text=text, context=state.context) == 'Нет':
                text_to_send = 'Попробуйте ещё раз'
                self.user_state.pop(user_id)
            if next_step['next_step']:  # если у "step2" есть "next_step"
                state.step_name = step['next_step']  # то в стейт записывается step_name="step2"
            else:
                self.user_state.pop(user_id)

        elif handler(text=text, context=state.context):
            # следующий шаг
            text_to_send = next_step['text'].format(**state.context)  # "Куда летим"
            if next_step['next_step']:  # если у "step2" есть "next_step"
                state.step_name = step['next_step']  # то в стейт записывается step_name="step2"
            else:
                self.user_state.pop(user_id)
        else:
            text_to_send = step['failure_text'].format(**state.context)
        return text_to_send


if __name__ == '__main__':
    logging_configurate()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
