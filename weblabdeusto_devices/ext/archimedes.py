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

