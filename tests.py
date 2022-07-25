from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from chatbot import Bot


class Test1(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1589640530, 'from_id': 12793114, 'id': 147, 'out': 0, 'peer_id': 12793114,
                               'text': 'зкшмуе', 'conversation_message_id': 144, 'fwd_messages': [], 'important': False,
                               'random_id': 0, 'attachments': [], 'is_hidden': False},
                   'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'],
                                   'keyboard': True, 'inline_keyboard': True, 'lang_id': 0}},
        'group_id': 194086943,
        'event_id': '771808878dae5fb281d8a0a2baf4778aa4477cf9'}

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poler_mock = Mock(return_value=events)
        long_poler_listen_mock = Mock()
        long_poler_listen_mock.listen = long_poler_mock

        with patch('chatbot.vk_api.VkApi'):
            with patch('chatbot.VkBotLongPoll', return_value=long_poler_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        send_mock = Mock()

        with patch('chatbot.vk_api.VkApi'):
            with patch('chatbot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(
            message=self.RAW_EVENT['object']['message']['text'],
            random_id=ANY,
            peer_id=self.RAW_EVENT['object']['message']['peer_id']
        )
