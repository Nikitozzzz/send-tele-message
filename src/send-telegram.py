import argparse
from telebot import TeleBot
import os
from tools import *


def main(args, message):
    config = read_config(args.config)

    if args.set_token:
        set_token(config)

    if args.add_chat:
        add_chat(config)

    if args.print_chats:
        print_chats(config)

    if args.remove_chat:
        remove_chat(config)

    if args.set_default_chat:
        set_default_chat(config)

    chat_id = None
    if args.chat:
        if args.chat.isdecimal():
            chat_id = args.chat
        else:
            chat_id = config['chats'].get(args.chat)
    else:
        if config['default_chat'] != '' and config['chats'].get(config['default_chat']):
            chat_id = config['chats'][config['default_chat']]
            

    if config['token'] and chat_id and (message or args.file or args.image or args.audio):
        try:
            bot = TeleBot(config['token'])
            
            if args.file and os.path.exists(args.file):
                with open(args.file, 'rb') as f:
                    bot.send_document(chat_id, f, caption=message)
            elif args.image and os.path.exists(args.image):
                with open(args.image, 'rb') as f:
                    bot.send_photo(chat_id, f, caption=message)
            elif args.audio and os.path.exists(args.audio):
                with open(args.audio, 'rb') as f:
                    bot.send_audio(chat_id, f, caption=message)
            else:
                bot.send_message(chat_id, message)
            
            
        except Exception as e:
            print(f'Ошибка: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Send message over telegram')
    initArgParser(parser)    

    args, message = parser.parse_known_args()

    main(args, ' '.join(message))
