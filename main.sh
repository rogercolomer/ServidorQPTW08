#!/bin/sh

python3 /home/roger/repositori/ServidorQPWood/Biomassa/lecturaBacnet.py &
python3 /home/roger/repositori/ServidorQPWood/Telegram/botTelegram.py &
python3 /home/roger/repositori/ServidorQPWood/Telegram/alarmesProduccio.py &
python3 /home/roger/repositori/ServidorQPWood/Telegram/alarmesTelegram.py &
python3 /home/roger/repositori/ServidorQPWood/main.py &
