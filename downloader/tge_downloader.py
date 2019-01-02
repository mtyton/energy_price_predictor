import requests
from lxml import html
import datetime

class Tge:
    """
    you shuold remember that downloader downloads data for next day
    so for date: dd.mm.yyyy
    downloads data for dd+1.mm.yyy
    """
    def __init__(self, date):
        # date format - yyyy-mm-dd
        self.date = date
        self.url = "https://gaz.tge.pl/pl/rdn/tgebase/?date={}".format(date)

    def get_data(self):
        """
        :return: - prices for a specific day
        """
        response = requests.get(self.url)
        doc = html.document_fromstring(response.text)
        hours, prices, volumes = self.extract_data(doc)
        data=[]
        for i in range(24):
            data.append({'hour':hours[i+1], 'price':prices[i+1], 'volume':volumes[i+1]})
        return data

    def extract_data(self, doc):
        """
        downloads data from website
        :param doc:
        :return:
        """
        price_elem = doc.cssselect("[class=wrap]")
        hour_elem = doc.cssselect("[class=header]")
        volume_elem = doc.cssselect("[class=volumes]")
        hours = self.get_hours(hour_elem)
        prices = self.get_prices(price_elem)
        volumes = self.get_volume(volume_elem)
        return hours, prices, volumes

    def get_hours(self, hour_elem):
        """
        :param hour_elem:
        :return: - list of hours
        """
        hours=[]
        for p in hour_elem:
            hours.append(p.text_content())
        return hours

    def get_volume(self, volume_elem):
        """
        :param volume_elem:
        :return: - transaction volume
        """
        volumes = []
        for v in volume_elem:
            name = v.text_content()
            name = name.split()
            name = name[-2]+name[-1]
            try:
                volumes.append(float(name))
            except:
                print("volume error")
        return volumes

    def get_prices(self, price_elem):
        """
        :param price_elem:
        :return: - list of prices
        """
        prices = []
        for p in price_elem:
            name = p.text_content()
            name = self.delete_whitespace(name)
            try:
                prices.append(float(name))
            except:
                pass
        return prices

    def delete_whitespace(self, word):
        """
        deletes whitespaces in strings
        :param word:
        :return:
        """
        new_word = ""
        for w in word:
            if w != " ":
                new_word += w
        return new_word

    def get_date(self):
        """
        :return: - date which is current set in downloader
        """
        return self.date

    def next_day(self):
        """
        changes day selected in loader
        :return: - new date
        """
        self.date += datetime.timedelta(days=1)
        self.url = "https://gaz.tge.pl/pl/rdn/tgebase/?date={}".format(str(self.date))
        return self.date

    def date_parser(self,str_date):
        """
        deprecated - can be deleted

        :param str_date:
        :return:
        """
        return datetime.datetime.strptime(str_date, "%Y-%m-%d")