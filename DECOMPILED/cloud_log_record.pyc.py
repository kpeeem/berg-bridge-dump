# 2016.01.27 00:42:35 MSK
import time
import json

class CloudLogRecord:

    def __init__(self, record):
        self.name = record.name
        self.message = record.message
        self.levelname = record.levelname
        self.levelno = record.levelno
        self.created = record.created
        self.process = record.process
        self.processName = record.processName



    def __repr__(self):
        return 'CloudLogRecord: created %s, name: %s, message %s' % (self.created, self.name, self.message)



    def to_hash(self):
        return {'name': self.name,
         'message': self.message,
         'levelname': self.levelname,
         'levelno': self.levelno,
         'created': self.created,
         'process': self.process,
         'processName': self.processName}



    @staticmethod
    def to_json(log_records, bridge_address_hex):
        json_records = []
        [ json_records.append(r.to_hash()) for r in log_records ]
        json_message = {'type': 'BridgeLog',
         'bridge_address': bridge_address_hex,
         'timestamp': time.time(),
         'records': json_records}
        return json.dumps(json_message)




+++ okay decompyling ./cloud_log_record.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:35 MSK
