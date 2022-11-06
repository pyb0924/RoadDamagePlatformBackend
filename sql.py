
import peewee


def query(param = [0,10,0,7,0],
          db=peewee.MySQLDatabase(host='localhost',
                     user='root',
                     password='lmk2000',
                     database='road',
                     charset='utf8'),
          sql = "select * from obj where loc1<%s and loc1>%S and loc2<%s and loc2>%s and type=%s"):
    #try:
        cursor = db.cursor()
        cursor.execute(sql,param)
        result = cursor.fetchall()
        cursor.close()
        #db.close()
        return result,cursor
    #except Exception:
        #print(0)

def edit_one(param = ['test_obj_id4',2,30.3,30.3,3],
             db=peewee.MySQLDatabase(host='localhost',
                                     user='root',
                                     password='lmk2000',
                                     database='road',
                                     charset='utf8'),
           sql="insert into obj values (%s,%s,%s,%s,%s)"):
    #try:
        cursor = db.cursor()
        cursor.execute(sql,param)
        db.commit()
        cursor.close()
        #db.close()
        #print(1)
    #except:
        #print(0)

def edit_multi(param = ['test_obj_id4',2,30.3,30.3,3],
               db=peewee.MySQLDatabase(host='localhost',
                                       user='root',
                                       password='lmk2000',
                                       database='road',
                                       charset='utf8'),
           sql="insert into obj values (%s,%s,%s,%s,%s)"):
    #try:
        cursor = db.cursor()
        cursor.executemany(sql,param)
        db.commit()
        cursor.close()
        #db.close()
        #print(1)
    #except:
        #print(0)
