from enum import Enum


class StatusEnum(str, Enum):
    '''Класс перечислений для статуса заказа'''
    in_process = 'В процессе'
    sent = 'Отправлен'
    delivered = 'Доставлен'
    