from math import sqrt

class Analysys:

    def __init__(self):
        self.alfa = 0.4
        self.beta = 0.4

    def get_prognose(self, trans):
        """
        returns prognose (price and volume) for next
        24 hours
        :param trans:
        :return:
        """
        results = []
        volumes, exvolumes = self.count_volumes(trans)
        prices, exprices = self.count_prices(trans)
        dict = self.change_to_dict(prices, volumes)
        price_mistakes, vol_mistakes = self.count_mistakes(prices, volumes, exprices, exvolumes)

        return dict, price_mistakes, vol_mistakes

    def count_prices(self, trans):
        """
        counts prognose price
        :param trans:
        :return:
        """
        result = []
        exresults, ft_list, st_list = self.count_exprices(trans)
        last_ft_list = self.get_last_day_trans(ft_list)
        last_st_list = self.get_last_day_trans(st_list)
        for i in range(24):
            result.append(self.count_real_prognose(last_ft_list[i], last_st_list[i], i))
        return result, exresults

    def count_exprices(self, trans):
        """
        counts previous prognose prices - neccesary for future price
        :param trans:
        :return:
        """
        exresults = []
        ft_list = []
        st_list = []
        exresults.append(trans[0]['price'])
        ft = trans[0]['price']
        ft_list.append(ft)
        st = 0
        st_list.append(st)
        for t in trans:
            ft = self.get_ft(t, ft, st, 'price')
            ft_list.append(ft)
            st = self.get_st(t, ft, ft_list[-2], st)
            st_list.append(st)
        exresults = self.join_lists(exresults, self.old_prices(ft_list, st_list))
        return exresults, ft_list, st_list

    def count_volumes(self, trans):
        """
        counts_current_volume
        :param trans:
        :return:
        """
        exresults, ft_list, st_list = self.count_exvolumes(trans)
        last_ft_list = self.get_last_day_trans(ft_list)
        last_st_list = self.get_last_day_trans(st_list)
        result = []
        for i in range(24):
            result.append(self.count_real_prognose(last_ft_list[i], last_st_list[i], i))
        return result, exresults

    def count_exvolumes(self, trans):
        """
        counts previous volumes
        :param trans:
        :return:
        """
        exresults = []
        ft_list = []
        st_list = []
        exresults.append(trans[0]['volume'])
        ft = trans[0]['volume']
        ft_list.append(ft)
        st = 0
        st_list.append(st)
        for t in trans:
            ft = self.get_ft(t, ft, st, 'volume')
            ft_list.append(ft)
            st = self.get_st(t, ft, ft_list[-2], st)
            st_list.append(st)
        exresults = self.join_lists(exresults, self.old_prices(ft_list, st_list))
        return exresults, ft_list, st_list

    def count_real_prognose(self, ft, st, i):
        """
        counts real prognose
        :param ft: - random fluctuations
        :param st: - trend
        :param i: - hour
        :return:
        """
        prognose =ft+(i-(i-1))*st
        return prognose

    def old_prices(self, ft_list, st_list):
        """
        counts before this day prices
        :param ft_list:
        :param st_list:
        :return:
        """
        results = []
        for i in range(1,len(st_list)):
            results.append(ft_list[i-1]+st_list[i-1])
        return results

    def count_mistakes(self, prices, volumes, exprices, exvolumes ):
        """
        mae - Mean Absolute Error
        mse - Mean Squadred Error
        rmse - Root Mean Square Error
        :param prices:
        :param volumes:
        :param exprices:
        :param exvolumes:
        :return:
        """
        vol_diff = self.get_difference(volumes, exvolumes, 'volume')
        price_diff = self.get_difference(prices, exprices, 'price')
        vol_abs_diff = self.count_abs(vol_diff)
        price_abs_diff = self.count_abs(price_diff)
        price_square_diff = self.count_square(price_diff)
        vol_square_diff = self.count_square(vol_diff)
        mae_vol = sum(vol_abs_diff)/24
        mae_price = sum(price_abs_diff)/24
        mse_vol = sum(vol_square_diff)/24
        mse_price = sum(price_square_diff)/24
        rmse_vol = sqrt(mse_vol)
        rmse_price = sqrt(mse_price)
        price_mistakes = [mae_price, mse_price, rmse_price]
        vol_mistakes = [mae_vol, mse_vol, rmse_vol]
        return price_mistakes, vol_mistakes

    def get_ft(self, tran, last_ft, last_st, type):
        """
        counts random fluctuations
        :param tran:
        :param last_ft:
        :param last_st:
        :return:
        """
        # ft = yesterad_price * alfa + (1 - alfa) * (last_ft + last_st)
        if type=='volume':
            amount = (tran['volume'] * self.alfa) + ((1-self.alfa)*(last_ft + last_st))
        else:
            amount = (tran['price'] * self.alfa) + ((1 - self.alfa) * (last_ft + last_st))
        return amount

    def get_st(self, tran, ft, last_ft, last_st):
        """
        counts trend
        :param tran:
        :param ft:
        :param last_ft:
        :param last_st:
        :return:
        """
        #st = beta*(ft - last_ft)+(1-beta)*last_st
        amount = (self.beta*(ft - last_ft)) + ((1-self.beta) * last_st)
        return amount

    def join_lists(self, list, second_list):
        """
        Simply joins two lists together
        :param list:
        :param second_list:
        :return:
        """
        new_list = list
        for elem in second_list:
            new_list.append(elem)
        return new_list

    def change_to_dict(self, prices, volumes):
        """
        transforms two lists to a dict
        :param prices:
        :param volumes:
        :return:
        """
        dict = []
        for i in range (24):
            hour = str(i) + '-' + str(i+1)
            dict.append({'hour': hour, 'price': prices[i], 'volume' : volumes[i-1]})
        return dict

    def get_last_day_trans(self, trans):
        """
        returns trans from last day
        :param trans: - means transactions
        :return:
        """
        help = trans
        new_trans = []
        for i in range(24):
            new_trans.append(help[-i-1])
        new_trans.reverse()
        return new_trans

    def get_difference(self, prices, exprices, type):
        """
        retruns diffrence between prognosed prices and known prices
        :param prices:
        :param exprices:
        :param type:
        :return:
        """
        diff = []
        if type == 'price':
            for i in range(24):
                diff.append(prices[i] - exprices[i])
        else:
            for i in range(23):
                diff.append(prices[i] - exprices[i])
        return diff

    def count_abs(self, elements):
        #abs - absolute
        new_elems = []
        for elem in elements:
            new_elems.append(abs(elem))
        return new_elems

    def count_square(self, elements):
        # counts second power of element
        new_elems = []
        for elem in elements:
            new_elems.append(pow(elem,2))
        return new_elems

    def get_price_data(self, file):
        transactions = []
        for line in file:
            (hour, price, volume) = line.split()
            transactions.append({'hour': hour, 'price': float(price), 'volume' : float(volume)})
        return transactions