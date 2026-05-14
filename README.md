# KSC Event Notifier for Max Bot
Отправляет уведомления о событиях Kaspersky Security Center в Max Bot.

## Установка 
Скачать последний релиз в виде испольняемого файла exe

## Настройка KSC
1. В свойствах серера администрирования необходимо включить запуск исполняемого файла
<img width="1629" height="914" alt="image" src="https://github.com/user-attachments/assets/d0e34e45-82c0-4c6b-b593-9f72c188fe61" />
2. Разделе "Управляемые устройства" редактируем политику "Сервер администрирования Kaspersky Security Center", для необходимых уведомлений включаем уведомление запуском исполняего файла
<img width="1398" height="814" alt="image" src="https://github.com/user-attachments/assets/dadc0e02-cccd-4efa-8241-55e79c4ada2c" />
! Примечание: по соображениям безопасности не рекомендуется производить сборку скрипта на сервере администрирования

## Аргументы запуска
Использование: ksc-max-bot-notifier.exe <chat_id> <bot_token> [loglevel]

Аргументы:
  chat_id     - ID чата в Max Bot (обязательный)
  bot_token   - Токен доступа к Max Bot API (обязательный)
  loglevel    - (опционально) уровень логирования: debug, info, warning, error, critical

Примеры:
  ksc-max-bot-notifier.exe 123456 token123
  ksc-max-bot-notifier.exe 123456 token123 warning
  ksc-max-bot-notifier.exe 123456 token123 debug
  ksc-max-bot-notifier.exe 123456 token123 error

Уровни логирования:
  debug    - Детальная отладочная информация
  info     - Информационные сообщения (по умолчанию)
  warning  - Только предупреждения и ошибки
  error    - Только ошибки
  critical - Только критические ошибки
  
  
## Самостоятельная сборка
cd ksc-max-bot-notifier
pip install -r requirements.txt
build.cmd
