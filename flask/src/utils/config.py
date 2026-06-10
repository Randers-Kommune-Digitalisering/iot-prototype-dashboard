import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

DEVELOPER_MODE = os.getenv('DEVELOPER_MODE', os.getenv('DEBUG', 'False')) in ['True', 'true']

OS2_API_BASE_URL = os.environ.get("OS2_IOT_API_BASE_URL", "https://os2iot-backend.prod.os2iot.kmd.dk/api/v1/")
OS2_API_KEY = os.environ.get("OS2_API_KEY")  # Required
OS2_APPLICATION_ID = os.environ.get("OS2_APPLICATION_ID")  # Required
OS2_DEVICE_PROFILE_ID = os.environ.get("OS2_DEVICE_PROFILE_ID")  # Required
OS2_DATA_TARGET_ID = os.environ.get("OS2_DATA_TARGET_ID")  # Required for Ento data export
OS2_VERIFY = os.environ.get("OS2_VERIFY", "True") in ["True", "true", "1"]  # Convert to boolean

# Validate types
if OS2_APPLICATION_ID:
    try:
        OS2_APPLICATION_ID = int(OS2_APPLICATION_ID)
    except ValueError:
        raise ValueError(f"OS2_APPLICATION_ID must be an integer if set, got: {OS2_APPLICATION_ID}")
if OS2_DATA_TARGET_ID:
    try:
        OS2_DATA_TARGET_ID = int(OS2_DATA_TARGET_ID)
    except ValueError:
        raise ValueError(f"OS2_DATA_TARGET_ID must be an integer if set, got: {OS2_DATA_TARGET_ID}")
