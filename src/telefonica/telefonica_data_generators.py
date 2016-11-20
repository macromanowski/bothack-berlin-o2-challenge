from random import randint
from random import randrange
from datetime import datetime

def generate_roaming_minutes():
    return randint(0, 180)


def generate_used_minutes():
    return randint(0, 600)


def generate_sent_sms():
    return randint(0, 5000)


def generate_outbund_minutes(max_range):
    '''

    :param max_range: max minutes
    :type int
    :return:
    '''

    return randint(0, max_range)


def generate_last_call_as_str():
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    phone_number = str(randint(100, 555)) + '-' + str(randint(100, 555)) + '-' + str(randint(100, 555))
    return date, phone_number


def generate_tariffe_limits_in_bytes(max_limit=1000000000):
    return randint(0, max_limit)

def generate_current_bill():
    return randrange(0.0, 120.0)