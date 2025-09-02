import os
from dotenv import load_dotenv
load_dotenv()
# ===============================
# ERPNext Related Configs
# ===============================
ERPNEXT_API_KEY = os.getenv("ERPNEXT_API_KEY")
ERPNEXT_API_SECRET = os.getenv("ERPNEXT_API_SECRET")
ERPNEXT_URL = os.getenv("ERPNEXT_URL")
ERPNEXT_VERSION = int(os.getenv("ERPNEXT_VERSION") or 14)

# ===============================
# Operational Configs
# ===============================
PULL_FREQUENCY = 20  # in minutes
LOGS_DIRECTORY = 'logs'  # logs of this script are stored in this directory
IMPORT_START_DATE = None  # format: 'YYYYMMDD'

# ===============================
# Biometric Device Configs
# 
# Notes:
# - device_id: Unique, strictly alphanumerical (no spaces)
# - ip: IP address of the device
# - punch_direction: 'IN', 'OUT', 'AUTO', or None
# - clear_from_device_on_fetch: Deletes punch data after fetch if True (⚠️ risk of data loss)
# - latitude & longitude: Required if 'Allow Geolocation Tracking' is enabled
# ===============================
devices = [
    {
        'device_id': 'ZKP01',
        'ip': '192.168.100.180',
        'port': 4370, 
        'punch_direction': None,
        'clear_from_device_on_fetch': False,
        'latitude': 0.0000,
        'longitude': 0.0000,
    },
    {
        'device_id': 'ZKP02',
        'ip': '192.168.100.176',
        'port': 43700,
        'punch_direction': None,
        'clear_from_device_on_fetch': False,
        'latitude': 0.0000,
        'longitude': 0.0000,
    }
]

# ===============================
# Shift Type Mapping for Sync
# 
# Purpose: Update "Last Sync of Checkin" in Shift Type Doctype
# Ref: https://discuss.erpnext.com/t/v-12-hr-auto-attendance-purpose-of-last-sync-of-checkin-in-shift-type/52997
# ===============================
shift_type_device_mapping = [
    {
        'shift_type_name': [
            'Malam 17:00-22:00',
            'Malam 23:00-04:00',
            'Malam 23:00-07:00',
            'Pagi 07:00-12:00',
            'Pagi 07:00-15:00',
            'Pagi 08:00-13:00',
            'Pagi 08:00-16:00',
            'Siang 12:00-17:00',
            'Siang 15:00-23:00',
            'Sore 15:00-20:00',
        ],
        'related_device_id': ['ZKP01', 'ZKP02'],
    }
]

# ===============================
# Allowed Exceptions from ERPNext
# 
# Ignored during sync:
# 1 - No Employee found
# 2 - Employee is inactive
# 3 - Duplicate Checkin
# All other exceptions will stop the sync process.
# ===============================
allowed_exceptions = [1, 2, 3]
