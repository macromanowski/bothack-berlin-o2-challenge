import requests
import tariffe
from exceptions import TelefonicaApiException
import telefonica_data_generators as data_generator


def __make_telefonica_get_request_for(telefonica_user_id):
    response = requests.get('http://api.bothack.io/telefonica/users/' + str(telefonica_user_id))
    response.raise_for_status()
    return response.json()


def get_information_for_user(user_id):
    try:
        user_data = __make_telefonica_get_request_for(user_id)
        telefonica_user_information = TelefonicaInformation(user_data)
        return telefonica_user_information
    except Exception as ex:
        print "error has occured : " + ex.message
        raise TelefonicaApiException(ex.message)


class TelefonicaInformation:
    area = None

    additional_data_booked = None
    additional_sms_packed = None

    tariff = None
    tariff_detail = None
    tariff_nice_name = None
    tariff_price = None
    tariff_duration = None
    tariff_date_left = None
    tariff_start_date = None

    user_age = None
    user_date_of_birth = None

    data_usage_month_in_bytes = None
    data_usage_three_months_in_bytes = None

    current_bill = data_generator.generate_tariffe_limits_in_bytes()

    def __init__(self, json):
        self.area = json['ar']
        self.additional_data_booked = (json['dp'] == 'Y')
        self.additional_sms_packed = (json['sm'] == 'Y')
        self.tariff = json['tr']
        self.tariff_detail = json['td']
        self.__load_tariffe_data(json)
        self.tariff_date_left = json['ep']
        self.tariff_start_date = json['fr']
        self.user_age = json['ag']
        self.user_date_of_birth = json['app']

        self.data_usage_month_in_bytes = json['du30']
        self.data_usage_three_months_in_bytes = json['du90']

        self.tariff_data_limits = data_generator.generate_tariffe_limits_in_bytes(4000000000)
        print 'data limits: ' + str(self.tariff_data_limits)
        print 'data usage:' + str(self.data_usage_month_in_bytes)
        print 'equals: ' + str(self.tariff_data_limits - self.data_usage_month_in_bytes)
        print 'bool: ' + str(self.tariff_data_limits - self.data_usage_month_in_bytes < 0)
        self.is_not_enough_data = self.tariff_data_limits - self.data_usage_month_in_bytes < 0

        self.is_already_above_limits = self.tariff_price - data_generator.generate_current_bill() < 0

    def __load_tariffe_data(self, json):
        tariffe_db = tariffe.TariffeDatabase()
        if self.tariff is None:
            return

        tariffe_detailed = tariffe_db.find_information_for_tariffe(self.tariff)
        if tariffe_detailed is None:
            print "There is no information for tariffe: " + self.tariff
            self.tariff_nice_name = self.tariff_detail
            self.tariff_price = 20.0
            self.tariff_duration = 24
            return

        self.tariff_nice_name = tariffe_detailed.nice_name
        self.tariff_price = tariffe_detailed.price
        self.tariff_duration = tariffe_detailed.duration



