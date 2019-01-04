
import time


def serialize(objt):
    if isinstance(objt, list):
        listtwo = []
        for item in objt:
            listtwo.append(serialize(item))
        return listtwo
    else: return objt.__dict__
 
def generate_id():
   now = time.time()
   localtime = time.localtime(now)
   milliseconds = '%03d' % int((now - int(now)) * 1000)
   return int(time.strftime('%Y%m%d%H%M%S', localtime) + milliseconds)

