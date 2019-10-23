from datetime import time

BASKET_COUNT = 10


class Basket(object):
    def __init__(self, border):
        self.border = border
        self.max_val = 0


class Interval(object):
    def __init__(self, start_time: time):
        self.delta = []
        self.start_time = start_time
        self.basket = []

    @staticmethod
    def print_title(f):
        f.write('time,count,min,max,avg')
        percent = .0
        delta_percent = 100.
        for _ in range(BASKET_COUNT):
            delta_percent /= 2
            percent += delta_percent
            f.write(',{:.3f}%'.format(percent))
        f.write('\n')

    def add_point(self, delta):
        self.delta += [delta]

    def write_to_file(self, f):
        n = len(self.delta)
        f.write(self.start_time.strftime('%T,'))
        f.write('{},'.format(n))
        self.delta = sorted(self.delta)
        f.write('{},'.format(self.delta[0]))  # min
        f.write('{},'.format(self.delta[-1]))  # max
        f.write('{}'.format(sum(self.delta) // n))  # avg

        border = .0
        for _ in range(BASKET_COUNT):
            border += (n - border) / 2
            self.basket += [Basket(border)]

        sum_val = .0
        i = 0
        for val in self.delta:
            sum_val += val
            for b in self.basket:
                if i < b.border:
                    b.max_val = val
                    break

            i += 1

        # put correct values in 'empty' baskets
        good_max_val = 0
        for b in self.basket:
            if b.max_val > 0:
                good_max_val = b.max_val
            f.write(',{}'.format(good_max_val))

        f.write('\n')
