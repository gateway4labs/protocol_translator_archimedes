import sys

STATUS_COMMAND = 'ALLINFO:archimedes1:archimedes2:archimedes3:archimedes4:archimedes5:archimedes6:archimedes7'

def get_sensor_metadata(reservation_id, message):
    metadata = {
        "method" : "getSensorMetadata",
        "sensors" : []
    }
    
    for number in range(1, 8):
        sensor_metadata = {
                    "sensorId" : "tube-%s" % number,
                    "fullName" : "Test tube %s" % number ,
                    "description" : "The test tube where the ball #%s is" % number,
                    "webSocketType" : "text",
                    "produces" : "application/json",
                    "configuration" : [],
                    "accessMode" : { 
                         "type" : "push",
                         "nominalUpdateInterval" : 3000, # 3 seconds
                         "userModifiableFrequency" : False
                    },
                    "values" : [
                            {
                                   "name" : "level",
                                   "unit" : "cm",
                                   # "lastMeasured" : "2014-...",
                                   "rangeMinimum" : 0.0,
                                   "rangeMaximum" : 100.0,
                                   "rangeStep" : 0.1,
                                   "updateFrequency" : 3000, # 3 seconds
                            },
                            {
                                   "name" : "load",
                                   "unit" : "gr",
                                   # "lastMeasured" : "2014-...",
                                   "rangeMinimum" : 0.0,
                                   "rangeMaximum" : 100.0,
                                   "rangeStep" : 0.1,
                                   "updateFrequency" : 3000,
                            }
                    ]
           }
        metadata['sensors'].append(sensor_metadata)
           
    for number in range(1, 8):
        cam_metadata = {
                "sensorId" : "video-%s" % number,
                "fullName" : "Video Test Tube %s" % number,
                "description" : "Video stream for the test tube %s" % number,
                "webSocketType" : "binary",
                "singleWebSocketRecommended" : True,
                "produces" : "image/jpeg",
                "configuration" : [], # Nothing can be configured
                "accessMode" : {
                      "type" : "stream",
                      "nominalUpdateInterval" : 500, # 0.5 seconds
                      "userModifiableFrequency" : False
                },
                "values" : [
                      {
                           "name" : "front",
                           # "lastMeasured" : "2014-...",
                           "updateFrequency" : 500,
                      }
                ]
        }
        metadata['sensors'].append(cam_metadata)

    return metadata

import time
import random

SENSOR_MAP = {
    'tube-1' : 'archimedes1',
    'tube-2' : 'archimedes2',
    'tube-3' : 'archimedes3',
    'tube-4' : 'archimedes4',
    'tube-5' : 'archimedes5',
    'tube-6' : 'archimedes6',
    'tube-7' : 'archimedes7',
}

def extract_response_data(new_data, sensor_id):
    if sensor_id not in SENSOR_MAP:
        print SENSOR_MAP
        print >> sys.stderr, "sensor_id %s not found in table" % sensor_id
        return {}

    archimedes_id = SENSOR_MAP[sensor_id]
    if archimedes_id not in new_data:
        print new_data
        print >> sys.stderr, "archimedes_id %s not found in data" % archimedes_id
        return {}
    
    archimedes_data = new_data[archimedes_id]

    return {
        'valueNames' : ['level', 'load'],
        'data' : [ archimedes_data['level'], archimedes_data['load'] ],
        'lastMeasured' : [time.asctime(), time.asctime()]
    }

