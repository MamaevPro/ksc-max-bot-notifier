#!/usr/bin/env python3
# encoding: utf-8
"""
KSC Event Notifier for Max Bot API
Отправляет уведомления о событиях Kaspersky Security Center в Max Bot
"""

import os
import sys
import re
import logging
from datetime import datetime

import requests
import urllib3

# Константы для уровней логирования
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

# Настройка директории для логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Отключаем предупреждения о небезопасных HTTPS запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Настройка временной зоны
os.environ["TZ"] = "UTC+5"


class MaxBotNotifier:
    """Класс для отправки уведомлений в Max Bot"""
    
    def __init__(self, chat_id: str, token: str):
        """
        Инициализация отправителя
        
        Args:
            chat_id: ID чата в Max Bot
            token: Токен доступа к Max Bot API
        """
        self.chat_id = chat_id
        self.token = token
        self.api_url = 'https://platform-api2.max.ru/messages'
        logger.info(f"Инициализация Max Bot отправителя для чата: {chat_id}")
    
    def send_message(self, message: str) -> bool:
        """
        Отправка сообщения в Max Bot
        
        Args:
            message: Текст сообщения для отправки
            
        Returns:
            bool: True если отправка успешна, иначе False
        """
        headers={
            "Content-Type":"application/json", 
            "Authorization": self.token
        }
        params={"chat_id":self.chat_id}   
        data = {
            'text': message,
            'format': 'markdown'
        }
        
        try:
            logger.debug(f"Отправка сообщения в Max Bot: {message[:100]}...")
            response = requests.post(
                self.api_url,
                json=data,
                params=params,
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.ok:
                response_data = response.json()
                if 'message' in response_data:
                    logger.info("Сообщение успешно отправлено")
                    return True
                else:
                    logger.error(f"Неожиданный ответ API: {response_data}")
                    return False
            else:
                logger.error(f"Ошибка HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error("Таймаут при отправке запроса к Max Bot API")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка соединения с Max Bot API: {e}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к Max Bot API: {e}")
            return False
        except ValueError as e:
            logger.error(f"Ошибка парсинга JSON ответа: {e}")
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке сообщения: {e}")
            return False


def setup_logging(log_level: str = 'info') -> None:
    """
    Настройка системы логирования
    
    Args:
        log_level: Уровень логирования (debug, info, warning, error, critical)
    """
    level = LOG_LEVELS.get(log_level.lower(), logging.INFO)
    log_filename = f"{LOG_DIR}/ksc_notifier_{datetime.now().strftime('%Y%m%d')}.log"
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Настройка обработчиков
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    global logger
    logger = logging.getLogger(__name__)
    logger.info(f"Система логирования инициализирована с уровнем: {log_level.upper()}")
    logger.info(f"Лог-файл: {log_filename}")


def escape_ip(text: str) -> str:
    """Экранирование IP адреса для безопасного отображения"""
    if not text:
        return "не указан"
    try:
        return re.sub(r"\.", r"[.]", text)
    except Exception as e:
        logger.error(f"Ошибка при экранировании IP адреса: {e}")
        return text


def get_rate_smile(level: str) -> str:
    """Получение эмодзи и описания уровня события"""
    rate_map = {
        "1": "ℹ️ **Информационное сообщение**",
        "2": "💡 **Предупреждение**",
        "3": "❗️ **Сбой**",
        "4": "🆘 **Критическое событие**"
    }
    return rate_map.get(level, "❓ Неизвестный уровень")


def get_env_variable(var_name: str, default: str = "не указано") -> str:
    """Безопасное получение переменной окружения"""
    value = os.environ.get(var_name)
    if value is None:
        logger.warning(f"Переменная окружения {var_name} не найдена")
        return default
    return value if value.strip() else default


def print_usage() -> None:
    """Вывод справки по использованию"""
    print("""
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
""")


def parse_arguments():
    """
    Парсинг аргументов командной строки
    
    Returns:
        tuple: (chat_id, bot_token, log_level)
    """
    args = sys.argv[1:]
    
    if '-h' in args or '--help' in args or 'help' in args:
        print_usage()
        sys.exit(0)
    
    if len(args) < 2:
        print("Ошибка: Недостаточно аргументов командной строки")
        print_usage()
        sys.exit(1)
    
    chat_id = args[0]
    token = args[1]
    log_level = 'warning'
    
    # Поиск уровня логирования среди аргументов
    for arg in args[2:]:
        if arg.lower() in LOG_LEVELS:
            log_level = arg.lower()
            break
    
    return chat_id, token, log_level


def main():
    """Основная функция программы"""
    try:
        # Парсинг аргументов
        bot_chat_id, bot_token, log_level = parse_arguments()
        
        # Настройка логирования
        setup_logging(log_level)
        
        logger.info("="*60)
        logger.info("Запуск KSC Event Notifier для Max Bot")
        logger.info(f"Chat ID: {bot_chat_id[:5]}..., Уровень логирования: {log_level}")
        
        # Инициализация отправителя
        notifier = MaxBotNotifier(bot_chat_id, bot_token)
        
        # Сбор информации о событии
        logger.info("Сбор информации о событии KSC")
        
        severity_num = get_env_variable('%KLCSAK_EVENT_SEVERITY_NUM%', '0')
        lvl = get_rate_smile(severity_num)
        
        event_name = get_env_variable('%EVENT%')
        computer_name = get_env_variable('%COMPUTER%')
        host_ip = get_env_variable('HOST_IP')
        domain_name = get_env_variable('%DOMAIN%')
        rise_time = get_env_variable('RISE_TIME')
        description = get_env_variable('%DESCR%')
        
        # Логирование полученных данных (только на уровне debug)
        logger.debug(f"Данные события: severity={severity_num}, event={event_name}, "
                    f"computer={computer_name}, ip={host_ip}, domain={domain_name}")
        
        # Экранирование IP адреса
        if host_ip != "не указано":
            host_ip = escape_ip(host_ip)
        
        # Формирование сообщения
        message = f""" {lvl} **в KSC**:
⏱ {rise_time}
🌍 {computer_name} {domain_name} {host_ip}
++{event_name}++
{description}"""
        
        logger.info(f"Сформировано сообщение (уровень события: {severity_num})")
        logger.debug(f"Текст сообщения:\n{message}")
        
        # Отправка сообщения
        if notifier.send_message(message):
            logger.info("Программа успешно завершила работу")
            sys.exit(0)
        else:
            logger.error("Не удалось отправить сообщение")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
        sys.exit(0)
    except Exception as e:
        if 'logger' in globals():
            logger.critical(f"Критическая ошибка: {e}")
        else:
            print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    logger = None
    main()
