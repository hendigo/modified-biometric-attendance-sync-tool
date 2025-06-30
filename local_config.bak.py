
# ERPNext related configs
ERPNEXT_API_KEY = '92b8f10afa6fa1c'
ERPNEXT_API_SECRET = '965a2bbbde57eb4'
ERPNEXT_URL = 'https://erp.coppal.cloud'
ERPNEXT_VERSION = 15


# operational configs
PULL_FREQUENCY = 15 # in minutes
LOGS_DIRECTORY = 'logs' # logs of this script is stored in this directory
IMPORT_START_DATE = None # format: '20190501'

# Biometric device configs (all keys mandatory, except latitude and longitude they are mandatory only if 'Allow Geolocation Tracking' is turned on in Frappe HR)
    #- device_id - must be unique, strictly alphanumerical chars only. no space allowed.
    #- ip - device IP Address
    #- punch_direction - 'IN'/'OUT'/'AUTO'/None
    #- clear_from_device_on_fetch: if set to true then attendance is deleted after fetch is successful.
                                    #(Caution: this feature can lead to data loss if used carelessly.)
    #- latitude - float, latitude of the location of the device
    #- longitude - float, longitude of the location of the device
devices = [
    {'device_id':'ZKP01','ip':'192.168.100.180', 'punch_direction': None, 'clear_from_device_on_fetch': False, 'latitude':0.0000,'longitude':0.0000},
    {'device_id':'ZKP02','ip':'192.168.100.176', 'port': 43700, 'punch_direction': None, 'clear_from_device_on_fetch': False, 'latitude':0.0000,'longitude':0.0000}
]

# Configs updating sync timestamp in the Shift Type DocType 
# please, read this thread to know why this is necessary https://discuss.erpnext.com/t/v-12-hr-auto-attendance-purpose-of-last-sync-of-checkin-in-shift-type/52997
shift_type_device_mapping = [
    {'shift_type_name': ['Normal Shift','Normal Shift : Sabtu','Shift 1 Machining','Shift 1 Machining : Sabtu','Shift 2 Machining','Shift 2 Machining : Sabtu','Shift 1 Injection Plastic','Shift 1 Injection Plastic : Sabtu','Shift 2 Injection Plastic','Shift 2 Injection Plastic : Sabtu','Shift 3 Injection Plastic','Shift 3 Injection Plastic : Sabtu'], 'related_device_id': ['ZKP01','ZKP02']}
]


# Ignore following exceptions thrown by ERPNext and continue importing punch logs.
# Note: All other exceptions will halt the punch log import to erpnext.
#       1. No Employee found for the given employee User ID in the Biometric device.
#       2. Employee is inactive for the given employee User ID in the Biometric device.
#       3. Duplicate Employee Checkin found. (This exception can happen if you have cleared the logs/status.json of this script)
# Use the corresponding number to ignore the above exceptions. (Default: Ignores all the listed exceptions)
allowed_exceptions = [1,2,3]
