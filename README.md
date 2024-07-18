# Бот для просмотра и конвертации валют

Бот построен на инлайн кнопках, но так же поддерживает и управление командами.

В боте реализована локализация на двух языках(Eng, Rus), storage на nats-py, потенциально легкорасширяемый кэш на redis, отложенные задачи для обновления курса на taskiq, и все завернуто в докер 

### Для запуска:
- создайте файл .env согласно примеру .env.example
- укажите токен своего бота
- запустите docker compose

Все необходимые инструкции по работе с ботом есть в самом боте:
https://t.me/pulivilizatorbot

