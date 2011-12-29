'''
Created on 2011-12-28

@author: lei
'''

import os
import sqlite3

last_sync_snapshot_sql = \
'''
CREATE TABLE last_sync_snapshot 
(


)
'''

def init_db(db_path) :
    if db_path :
        with sqlite3.connect(path) as conn :
            pass