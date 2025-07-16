import json
import os
import re


HOME_DIR = os.path.expanduser('~')
CONFIG_DIR = os.path.join(HOME_DIR, '.send-tele-message')
DAFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

CONFIG_FILE = ''

_TOKEN_TEST = r'^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$'




if not os.path.exists(CONFIG_DIR):
    os.mkdir(CONFIG_DIR)


def initArgParser(parser):
    parser.add_argument('--chat', required=False)
    parser.add_argument('--add-chat', required=False, action='store_true', help='Add chat')
    parser.add_argument('--remove-chat', required=False, action='store_true', help='Remove chat')
    parser.add_argument('--print-chats', required=False, action='store_true', help='Print chat list')
    parser.add_argument('--set-default-chat', required=False, action='store_true', help='Set default chat')
    parser.add_argument('--set-token', required=False, action='store_true', help='Set token')
    parser.add_argument('--config', required=False)
    parser.add_argument('--file', required=False)
    parser.add_argument('--image', required=False)
    parser.add_argument('--audio', required=False)


def read_config(config_path=None):
    global CONFIG_FILE

    if config_path:
        CONFIG_FILE = config_path
    else:
        CONFIG_FILE = DAFAULT_CONFIG_FILE

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if type(config) == dict:
                if not config.get('token'):
                    config['token'] = ''
                if not config.get('chats'):
                    config['chats'] = {}
                if not config.get('default_chat'):
                    config['default_chat'] = ''

                return config
    
    return {
        'token': '',
        'chats': {},
        'default_chat': ''
    }

    
def write_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f)


def set_token(config):
    token = input('Введите токен: ')

    if not re.fullmatch(_TOKEN_TEST, token):
        print('Токен не соответствует принятому формату!')
        return
    
    config['token'] = token
    write_config(config)


def add_chat(config):
    chat = input('Введите название чата: ')
    if chat == '':
        print('Вы не указали имя чата')
        return

    chat_id = input('Введите chat_id: ')
    if not chat_id.isdigit():
        print('Chat_id должен быть числом.')
        return

    config['chats'][chat] = chat_id
    write_config(config)


def print_chats(config):
    if len(config['chats']) == 0:
        print('Чатов не найдено!')
        return
    

    print('Список сохраненных чатов: ')
    _print_chats(config)


def remove_chat(config):
    if len(config['chats']) == 0:
        print('Чатов не найдено!')
        return
    
    
    print('Выберите чат для удаления: ')
    _print_chats(config)

    num = input('> ')
    if not num.isdigit():
        print('Нужно было ввести число...')
        return
    
    num = int(num)

    if num > 0 and num <= len(config['chats']):
        del config['chats'][list(config['chats'])[num-1]]
        write_config(config)
    else:
        print('Чат не найден.')


def set_default_chat(config):
    if len(config['chats']) == 0:
        print('Чатов не найдено!')
        return
    
    print('Выберите чат по-умолчанию: ')
    _print_chats(config)

    num = input('> ')
    if not num.isdigit():
        print('Нужно было ввести число...')
        return
    
    num = int(num)

    if num > 0 and num <= len(config['chats']):
        config['default_chat'] = list(config['chats'])[num-1]
        write_config(config)
    else:
        print('Чат не найден.')



def _print_chats(config):
    for i, chat in enumerate(config['chats'], start=1):
        print(f'{i}) {chat}, id: {config["chats"][chat]}')
