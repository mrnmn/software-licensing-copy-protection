import psycopg2
from psycopg2 import sql
from datetime import date as get_date
#first create the devices table
'''
CREATE TABLE devices
(
  costumer_id BIGSERIAL NOT NULL PRIMARY KEY,
  email VARCHAR(50) UNIQUE,
  mac BIGINT UNIQUE DEFAULT NULL
);

-- trial table exemple if you want to use a separate table, But it needs some changes in the code.
-- this module works wuith one table for copy protection and free trial periods.

CREATE TABLE trial
(
 costumer_id BIGSERIAL NOT NULL PRIMARY KEY,
 email VARCHAR(50) UNIQUE,
 mac BIGINT UNIQUE DEFAULT NULL,
 start_date DATE DEFAULT NULL,
 end_date DATE DEFAULT NULL,
 status BOOLEAN DEFAULT FALSE
);

'''
# see main.py for how to use each function
#add new client, mac always NULL
def new_client(tablename:str,email:str,mac:None):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    make_state = sql.SQL("""INSERT INTO {tablename} (email, mac) VALUES({email},{mac})""").format(tablename= sql.Identifier(tablename), email = sql.Literal(email), mac = sql.Literal(mac))
    cur.execute(make_state)
    con.commit()
    #close connection
    cur.close()
    con.close()
    if is_email_exist(tablename,email):
        return True
    else:
        return False


# activate licence
# the mac comes as int (converted from hexa to int) 
def activate_license(tablename:str,email:str, mac:int):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET mac = CASE WHEN email ={email} AND mac IS NULL THEN {mac} ELSE mac END""").format(tablename =sql.Identifier(tablename), email=sql.Literal(email), mac= sql.Literal(mac))
    cur.execute(state)
    con.commit()
    
    #close connection
    cur.close()
    con.close()
    if is_mac_exist(tablename,mac):
        return True
    else:
        return False

#activate license after trial
def activate_license_after_trial(tablename:str,email:str, mac:int):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET mac = CASE WHEN email ={email} AND mac IS NULL AND status IS TRUE THEN {mac} ELSE mac END""").format(tablename =sql.Identifier(tablename), email=sql.Literal(email), mac= sql.Literal(mac))
    cur.execute(state)
    con.commit()
    #close connection
    cur.close()
    con.close()
    if is_mac_exist(tablename,mac):
        return True
    else:
        return False

#change device 
def change_device(tablename:str, email:str, mac:int):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET mac = CASE WHEN email={email} AND mac ={mac} AND status IS false THEN NULL ELSE mac END""").format(tablename =sql.Identifier(tablename) ,email= sql.Literal(email), mac = sql.Literal(mac))
    cur.execute(state)
    con.commit()
    #close connection
    cur.close()
    con.close()
    if not is_mac_exist(tablename,mac):
        return True
    else:
        return False

# check if the db ontains the mac adress
def is_mac_exist(tablename:str, mac:int):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""SELECT mac FROM {tablename} WHERE mac ={mac}""").format(tablename = sql.Identifier(tablename),mac=sql.Literal(mac))
    cur.execute(state)
    result = cur.fetchone()
    if(result!= None):
        return True
    else:
        return False
    cur.close()
    con.close()
 
 #Check if the email exists in the database.
def is_email_exist(tablename:str,email:str):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""SELECT email FROM {tablename} WHERE email ={email}""").format(tablename = sql.Identifier(tablename),email=sql.Literal(email))
    cur.execute(state)
    result = cur.fetchone()
    if(result!= None):
        return True
    else:
        return False

# add columns for trial version for the first time.
def set_trial_columns(tablename:str):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    # columns added if not exixts table, else just skipping!
    state = sql.SQL("""ALTER TABLE {tablename} ADD COLUMN IF NOT EXISTS start_date DATE DEFAULT NULL, ADD COLUMN IF NOT EXISTS end_date DATE DEFAULT NULL, ADD COLUMN IF NOT EXISTS status BOOLEAN DEFAULT FALSE""").format(tablename=sql.Identifier(tablename))
    cur.execute(state)
    con.commit()
    #close connection
    cur.close()
    con.close()
    return True 


# trial version, determine the trial period for the client (in days )
def set_trial(tablename:str, email:str, period:int):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET start_date = CASE WHEN email ={email} AND start_date IS NULL AND end_date IS NULL AND mac IS NOT NULL AND status IS false THEN CURRENT_DATE ELSE start_date END""").format( tablename = sql.Identifier(tablename),email =sql.Literal(email))
    make_state = sql.SQL("""UPDATE {tablename} SET end_date = CASE WHEN email = {email} AND end_date IS NULL AND mac IS NOT NULL AND status IS false THEN CURRENT_DATE + {period} ELSE end_date END""").format( tablename = sql.Identifier(tablename),email = sql.Literal(email), period = sql.Literal(period))
    try:
        cur.execute(state)
        con.commit()
        cur.execute(make_state)
        con.commit()
        print('start and end date saved in db.') #ignore if the periods already exists.
        return True
    except:
        print('cant add data.')
        return False
    #close connection
    cur.close()
    con.close()

#clear start date and end date columns if status is true (after the end of the trial period.)
def clear_periods(tablename:str, email:str):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET start_date = CASE WHEN email ={email} AND start_date IS NOT NULL AND end_date IS NOT NULL AND mac IS NOT NULL AND status IS true THEN NULL ELSE start_date END""").format( tablename = sql.Identifier(tablename),email = sql.Literal(email) )
    make_state = sql.SQL("""UPDATE {tablename} SET end_date = CASE WHEN email = {email} AND end_date IS NOT NULL AND mac IS NOT NULL AND status IS true THEN NULL ELSE end_date END""").format( tablename = sql.Identifier(tablename),email = sql.Literal(email))
    try:
        cur.execute(state)
        con.commit()
        cur.execute(make_state)
        con.commit()
        print('start and end date removed (status is true).') #ignore if the periods already exists.
        return True
    except:
        print('cant remove start and end date.')
        return False
    cur.close()
    con.close()

#chek if trial period expired / Exit the trial period.
def trial_expired(tablename:str, mac:int):
    today = get_date.today()
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""SELECT end_date FROM {tablename} WHERE mac = {mac}""").format( tablename = sql.Identifier(tablename),mac =sql.Literal(mac))
    cur.execute(state)
    result = cur.fetchone()
    for end_date in result:
        if today >= end_date:
            #get the email adress
             state = sql.SQL("""SELECT email FROM {tablename} WHERE mac = {mac}""").format(tablename = sql.Identifier(tablename),mac =sql.Literal(mac))
             try:
                 cur.execute(state)
                 email_result = cur.fetchone() 
                 for client_email in email_result:
                     if change_device(tablename,client_email, mac): # call change_device to remove the mac from db so the user will not be able to use the software. 
                         state = sql.SQL("""UPDATE {tablename} SET status = CASE WHEN email ={client_email} AND mac IS NULL THEN true ELSE status END""").format(tablename = sql.Identifier(tablename), client_email= sql.Literal(client_email))# change the status to true means the trial period is expired for this device.
                         cur.execute(state)
                         con.commit()
                         return True # return true,(trial period expired) the mac has been successfully removed , and the status is changed to true.
             except:
                 raise Exception("cant remove the mac adress./ modfy the status column.") # ERROR!
               
                    
        else:
            print('The trial period has not expired yet.')
            return False # return false, the trial period has not expired yet.

    #close connection
    cur.close()
    con.close()

# change the status for a client from trial to paid.
def trial_to_paid(tablename:str, email:str):
    con = psycopg2.connect(dbname='test', user='postgres', password='password', host='localhost')
    cur = con.cursor()
    state = sql.SQL("""UPDATE {tablename} SET status = CASE WHEN email = {email} AND status IS true THEN false END""").format( tablename = sql.Identifier(tablename),email =sql.Literal(email))
    try:
        cur.execute(state)
        con.commit()
        return True
    except:
        return False
