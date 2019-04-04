from downloader.tge_downloader import Tge
from predictor.data_analysys import Analysys
import matplotlib.pyplot as plt
import datetime
import argparse

def run():
    download_data()
    analyse_data()

def analyse_data():
    analyse = Analysys()  # Creates object of Analysys class
    file = open('dane.txt', 'r')
    trans = analyse.get_price_data(file)
    file.close()

    if trans:
        file = open('wyniki.txt', 'w')
        prognose, price_mistake, vol_mistake = analyse.get_prognose(trans)
        save_to_file(prognose, file, price_mistake, vol_mistake, get_current_download_date())
        file.close()
        trans = analyse.get_last_day_trans(trans)
        draw_func(prognose, trans)
    else:
        print("data reading error")

def download_data():
    file = open('dane.txt', 'a')
    max_date = get_current_download_date()  # get our current date
    date = get_date()
    if not date:
        date = datetime.datetime.utcnow() - datetime.timedelta(days=60)
    tge = Tge(date)  # creates tge object
    loop(tge, file, max_date)
    file.close()

def loop(api, file, date):
    """
    downloads data from given source
    :param api: - object of downloading class
    :param file: - file which we use to save data
    :return:
    """
    while date >= api.get_date():
        data = api.get_data()
        save_to_file(data, file)
        api.next_day()

def get_current_download_date():
    """
    :return: - date for which we should download
    """
    date = datetime.datetime.utcnow()
    download_hour = datetime.datetime.strptime("12:00:00", "%H:%M:%S")
    if not check_time(download_hour):
        date -= datetime.timedelta(days=1)
    return date

def get_date():
    """
    gets previous date saved in file
    :return:
    """
    data=[]
    file = open("wyniki.txt", "r")
    for line in file:
        data.append(line)
    date = datetime.datetime.strptime(data[-1], "%Y-%m-%d")
    file.close()
    return date

def check_time(download_hour):
    """
    check if hour after which u can download data has passed
    :param download_hour:
    :return:
    """
    if datetime.datetime.time(datetime.datetime.utcnow()) > datetime.datetime.time(download_hour):
        return True
    else:
        return False

def save_to_file(data, file, price_mistake=None, vol_mistake=None, date = None):
    """
    saves data given as parameters to file
    :param data:
    :param file:
    :return:
    """
    for item in data:
        file.write(str(item['hour']) + ' ' + str(item['price']) + ' ' + str(item['volume']))
        file.write('\n')

    if vol_mistake and price_mistake and date:
        file.write("Volume mistakes (mae, mse, rmse): ")
        file.write('\n')
        for mistake in vol_mistake:
            file.write(str(mistake))
            file.write('\n')

        file.write("price mistakes (mae, mse, rmse):")
        file.write('\n')
        for mistake in price_mistake:
            file.write(str(mistake))
            file.write('\n')
        date += datetime.timedelta(days=1)
        file.write(str((date.date())))

def draw_func(data, trans):
    """
     drawing a plot using a matplotlib library
    :param data:
    :return:
    """
    x = []
    y = []
    y_sec=[]
    for d in data:
        x.append(d['hour'])
        y.append(d['price'])
    for t in trans:
        y_sec.append(t['price'])

    plt.plot(x, y, label="prediction")
    plt.plot(x, y_sec, label="current prices")
    plt.legend()
    plt.show()

if __name__=="__main__":
    run()
