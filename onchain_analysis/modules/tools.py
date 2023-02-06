from datetime import datetime as dt
from datetime import timezone
import numpy
class Tools():

    @staticmethod
    def counter(func):
        def wrapper(*args, **kwargs):
            count = 0
            result = []
            while count < kwargs['limit']: ##get count limit num from func argument
                kwargs['num_of_times'] = count ## pass number of run times to func
                result.extend(func(*args, **kwargs))
                count += 1
            return result
        return wrapper


    @staticmethod
    def datetime_to_timestamp(timeString: str):
       return int(dt.strptime(timeString, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())




































