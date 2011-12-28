'''
Created on 2011-12-28

@author: lei
'''

import os
import sqlite3

def init_db(db_path) :
    if db_path :
        with sqlite3.connect(path) as conn :
            pass