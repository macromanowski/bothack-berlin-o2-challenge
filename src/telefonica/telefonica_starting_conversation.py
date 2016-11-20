import telefonica
import telefonica_data_generators as random_data


class BasicIntroduction(object):
    facebook_id = None
    telefonica_id = 1  # can be changed via REST API
    tariffe_info = None

    def __init__(self, facebook_id):
        self.facebook_id = facebook_id
        self.tariffe_info = telefonica.get_information_for_user(self.telefonica_id)

    def get_basic_plan_information(self):
        telefonica_information = telefonica.get_information_for_user(self.telefonica_id)

        available_data = float(telefonica_information.tariff_data_limits / 1000000000)

        return telefonica_information.tariff_nice_name, available_data, telefonica_information.tariff_price

    def is_not_enough_data(self):
        return self.tariffe_info.is_not_enough_data

    def is_already_above_limits(self):
        return self.tariffe_info.is_already_above_limits

    def minutes_above_plan(self):
        return str(random_data.generate_outbund_minutes(120))

    def sms_above_plan(self):
        return str(random_data.generate_sent_sms())

    def get_user_age(self):
        return self.tariffe_info.user_age

