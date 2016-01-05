import pymssql,psycopg2

def FetchOneSQL(query,serverUrl='',user='',pwd=''):
    cnxn = pymssql.connect(serverUrl,user,pwd)
    cursor = cnxn.cursor()
    cursor.execute(query)
    response = cursor.fetchone()
    cursor.close()
    cnxn.close()
    return response
def FetchAllSQL(query,serverUrl='',user='',pwd=''):
    cnxn = pymssql.connect(serverUrl,user,pwd)
    cursor = cnxn.cursor()
    cursor.execute(query)
    response = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return response
def CommitQuerySQL(query,serverUrl='',user='',pwd=''):
    cnxn = pymssql.connect(serverUrl,user,pwd)
    cursor = cnxn.cursor()
    cursor.execute(query)
    cnxn.commit()
    cnxn.close()
def FetchAllPostgres(query,connect_string=''): # connect_string="host='%s' dbname='%s' user='%s' password='%s'"
    conn = psycopg2.connect(connect_string)    # where Host is localhost or a url to the server, dbName is DatabaseName
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def FetchOnePostgress(query,connect_string=''):
    conn = psycopg2.connect(connect_string) 
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result