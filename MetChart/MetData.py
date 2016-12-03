import ujson
import os
import pkg_resources
import logging
from datetime import datetime

REGION_FIELD = pkg_resources.resource_filename(__name__, "data")

logger = logging.getLogger()

class MetData(object):
    
    def __init__(self):

        self.data = {}
        self._load_from_file()

    def _load_from_file(self):

        data_file = os.path.join(REGION_FIELD, 'daily_16.json')

        logger.info("Loading met data from file: {}".format(data_file))
        with open(data_file, 'r') as fp:
            for line in fp.readlines()[:]:
                obj = ujson.loads(line)
                name = obj['city']['name'].encode('ascii', 'ignore')

                logger.debug("Loading City Data: {}".format(name))

                self.data[name] = [] 
                for item in obj['data']:
                    dest = {}
                    dest['date'] = datetime.fromtimestamp(item['dt']).date()
                    for key in ['clouds', 'rain', 'humidty']:
                        if key in item:
                            dest[key] = item[key]
                    if 'temp' in item:
                        dest['tmax'] = item['temp']['max'] - 273.15
                        dest['tmin'] = item['temp']['min'] - 273.15
                        dest['tavg'] = item['temp']['day'] - 273.15

                    if dest:
                        self.data[name].append(dest)

        logger.info("Finished loading Met data")


    def get_timeseries(self, **kwargs):

        name = kwargs['name']
        var = kwargs['var'] 

        if name not in self.data:
            raise KeyError("Unknown name: {}".format(name))

        if var not in self.data[name][0]:
            raise KeyError("Variable: {} not available for: {}".format(var, name))
           
        x_data = []
        y_data = []
        for i in [j for j in self.data[name] if (var in j)]:
            x_data.append(i['date'])
            y_data.append(i[var])

        return x_data, y_data
            





