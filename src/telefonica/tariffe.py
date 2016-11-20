import xml.etree.ElementTree as ET
import os
import random


class TariffeDatabase:
    data = None

    def __init__(self):
        self.data = ET.parse(os.path.relpath('tarife.xml'))

    def find_information_for_tariffe(self, tariffe_name):
        '''

        :param tariffe_name: tariffe name from JSON
        :type tariffe_name: str
        :return: information about tariffe
        :rtype TariffeInformation:
        '''
        root = self.data.getroot()
        for tariff in root:
            if (tariff.find('.//{http://www.o2online.de/xmlfeeds/v4/tariffs}name').text == tariffe_name):
                return TariffeInformation(tariff)

        return None

    def get_random_tariff(self):
        '''

                :param tariffe_name: tariffe name from JSON
                :type tariffe_name: str
                :return: information about tariffe
                :rtype TariffeInformation:
                '''
        root = self.data.getroot()
        tariffe_number = random.randint(1, 10)
        selected_data = TariffeInformation(root.findall('.//{http://www.o2online.de/xmlfeeds/v4/tariffs}tariff')[tariffe_number])
        return selected_data.nice_name, selected_data.price, selected_data.duration


class TariffeInformation:
    nice_name = None
    price = None
    duration = None

    def __init__(self, tariffe_node):
        self.nice_name = tariffe_node.find('.//{http://www.o2online.de/xmlfeeds/v4/tariffs}description').text
        if tariffe_node.find('..//{http://www.o2online.de/xmlfeeds/v4/tariffs}pricing/{http://www.o2online.de/xmlfeeds/v4/tariffs}price/{http://www.o2online.de/xmlfeeds/v4/tariffs}rc') == None:
            self.price = 20.0
        else:
            self.price = tariffe_node.find('..//{http://www.o2online.de/xmlfeeds/v4/tariffs}pricing/{http://www.o2online.de/xmlfeeds/v4/tariffs}price/{http://www.o2online.de/xmlfeeds/v4/tariffs}rc').text

        if tariffe_node.find('..//{http://www.o2online.de/xmlfeeds/v4/tariffs}pricing/{http://www.o2online.de/xmlfeeds/v4/tariffs}price/{http://www.o2online.de/xmlfeeds/v4/tariffs}numRC') == None:
            self.duration = 24
        else:
            self.duration = tariffe_node.find('..//{http://www.o2online.de/xmlfeeds/v4/tariffs}pricing/{http://www.o2online.de/xmlfeeds/v4/tariffs}price/{http://www.o2online.de/xmlfeeds/v4/tariffs}numRC').text
