# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:23:49 2018

@author: tony.zhao2
"""

import os
import re
import pandas as pd
import Signal_of_one_file


class Signals_all(object):
    def __init__(self):
        self.data = pd.DataFrame()

    def add_one_file(self, filepath):
        one_signal = Signal_of_one_file.Signal_of_one_file()
        one_signal.add_file(filepath)
        self.data = self.data.append(one_signal._data)
        return one_signal.get_CE()

    def add_all(self, directory_in_str):
        directory = os.fsencode(directory_in_str)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                CE = re.match(r'.+00(?P<CE>\d+).txt', filename).group('CE')
                CE = float(CE)
                if self.add_one_file('%s\%s' % (directory_in_str, filename)) != CE:
                    print("CE not match.")

        return self.data


if __name__ == "__main__":
    sa = Signals_all()
    sa.add_all('.\922-230')
    sa.data.to_csv("all_signal.csv")
