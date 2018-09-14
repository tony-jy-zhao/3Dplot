# -*- coding: utf-8 -*-

' parse GraphP():Save() file using regex & pandas.DataFrame. Could be extended to more file types '

__author__ = "JTZ"

import re
import pandas as pd
import Draw_2d

_genericDecNum = '[-+]?\d*\.\d+|\d+'
rx_dict = {
    'CE': re.compile(r'.+Fix = (?P<CE>\d+)'),
    'Q2RF&Intensity': re.compile(r'(?P<q2rf>%s)[ \t](?P<intensity>%s)' % (_genericDecNum, _genericDecNum))
}

smooth_flag = True

def _parse_line(line):
    """
    regex search
    """
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_file(filepath):
    data = []
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            key, match = _parse_line(line)
            if key == 'CE':
                CE = match.group('CE')
                CE = float(CE)

            if key == 'Q2RF&Intensity':
                q2rf = match.group('q2rf')
                q2rf = float(q2rf)
                intensity = match.group('intensity')
                intensity = float(intensity)

                row = {
                    'CE': CE,
                    'Q2RF': q2rf,
                    'Intensity': intensity
                }
                data.append(row)

            line = file_object.readline()

        data = pd.DataFrame(data)
        data.set_index(['CE', 'Q2RF'], inplace=True)
        # check for duplicated indexes
        # https://stackoverflow.com/questions/13035764/remove-rows-with-duplicate-indices-pandas-dataframe-and-timeseries
        data = data.groupby(level=data.index.names)

        # .first() || .last()
        if smooth_flag:
            data = data.last()

        else:
            data = data.first()

    return data


if __name__ == '__main__':
    filepath = '922-230\graph_0012.txt'
    data = parse_file(filepath)
    # data.to_csv('a_signal.csv')
    print(data)
