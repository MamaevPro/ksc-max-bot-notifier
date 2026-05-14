# KSC-Max-bot-notifier
Отправляет уведомления о событиях Kaspersky Security Center в мессенджер Max.

## Установка и запуск

### Быстрый старт (простой способ)
1. Скачайте [последнюю версию ksc-max-bot-notifier.exe](https://github.com/MamaevPro/ksc-max-bot-notifier/releases/tag/ksc-max-bot-notifier)
2. Произведите настройку KSC согласно инструкции ниже

###  Самостоятельная сборка исполняемого файла (рекомендуемый способ)
Для сборки необходим [Python 3 for Windows](https://www.python.org/downloads/windows/). Вместо команды `git clone` репозиторий можно просто скачать:
<img width="409" height="355" alt="image" src="https://github.com/user-attachments/assets/e4fb3afa-bf1b-4f6f-b7ae-85fb2fcb76d1" />

**Команды для сборки:**
```git clone https://github.com/MamaevPro/ksc-max-bot-notifier/
cd ksc-max-bot-notifier
pip install -r requirements.txt
build.cmd
```

## Настройка Kaspersky Security Center
1. В свойствах **Сервера администрирования**, на вкладке **Уведомления** необходимо включить запуск исполняемого файла, выбрать исполняемый файл, указать идентификатор чата и токен бота.
<img width="1629" height="914" alt="image" src="https://github.com/user-attachments/assets/d0e34e45-82c0-4c6b-b593-9f72c188fe61" />

2. Разделе **Управляемые устройства** редактируем политику **Сервер администрирования Kaspersky Security Center**, для необходимых уведомлений включаем уведомление запуском исполняего файла.
<img width="1398" height="814" alt="image" src="https://github.com/user-attachments/assets/dadc0e02-cccd-4efa-8241-55e79c4ada2c" />

**Примечание: в целях безопасности не рекомендуется производить сборку скрипта на сервере администрирования**

## Аргументы запуска
Использование: `ksc-max-bot-notifier.exe <chat_id> <bot_token> [loglevel]`

**Аргументы**:
1. `chat_id`     - ID чата в Max (обязательный). В [веб-версии](https://web.max.ru) `chat_id` отображается в конце строки URL
2. `bot_token`   - Токен доступа к Max Bot API (обязательный)
3. `loglevel`    - (опционально) уровень логирования: debug, info, warning, error, critical

**Примеры**:
```
ksc-max-bot-notifier.exe 123456 token123
ksc-max-bot-notifier.exe 123456 token123 critical
ksc-max-bot-notifier.exe 123456 token123 debug
ksc-max-bot-notifier.exe 123456 token123 error
```
**Уровни логирования**:
1. `debug`    - Детальная отладочная информация
2. `info`     - Информационные сообщения
3. `warning`  - Только предупреждения и ошибки (по умолчанию)
4. `error`    - Только ошибки
5. `critical` - Только критические ошибки

## Пример работы
<img width="496" height="408" alt="image" src="https://github.com/user-attachments/assets/4b609b54-0016-4b7d-b7f1-7bbae5557b5b" />

