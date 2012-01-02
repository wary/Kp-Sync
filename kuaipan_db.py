'''
Created on 2011-12-28

@author: lei
'''

import os
import sqlite3

KFile_sql = \
'''
CREATE TABLE KFile 
(
fileId VARCHAR(100) PRIMARY KEY,
name VARCHAR(260),
type VARCHAR(10),
parentId VARCHAR(100),
sha1 VARCHAR(42),
size VARCHAR(100),
modTime VARCHAR(100),
createdTime VARCHAR(100),
shared VARCHAR(100),
fileVer VARCHAR(100),
opVer VARCHAR(100),
path VARCHAR(1000)
)
'''

def get_conn() :
    return sqlite3.connect('sync.db')

def init_db() :
    if db_path :
        with get_conn() as conn :
            conn.execute(KFile_sql)

def save_object(object,table_name) :
    property_list = get_table_columns(table_name)
    sql = 'insert into % s values ( %s )' % \
            (table_name,','.join(['?' for i in xrange(len(property_list))]))
    with get_conn() as conn :
        conn.execute(sql,[hasattr(object, property) and getattr(object, property) or '' 
                          for property in property_list])    
        
    
def get_table_columns(table_name) :
    with get_conn() as conn :
            return [row[1] for row in conn.execute('pragma table_info(%s)' % table_name)]  
    
     
    

            


if __name__ == '__main__':
    #init_db('sync.db')
    print save_object(None,'KFile')
    print 'done!'