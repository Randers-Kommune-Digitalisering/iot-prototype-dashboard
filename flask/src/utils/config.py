import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

OS2_API_BASE_URL = os.environ.get("OS2_IOT_API_BASE_URL", "https://os2iot-backend.prod.os2iot.kmd.dk/api/v1/")
OS2_API_KEY = os.environ.get("OS2_API_KEY")  # Required
OS2_APPLICATION_ID = int(os.environ.get("OS2_APPLICATION_ID"))  # Required
OS2_DEVICE_PROFILE_ID = os.environ.get("OS2_DEVICE_PROFILE_ID")  # Required
OS2_VERIFY = os.environ.get("OS2_VERIFY", "True") in ["True", "true", "1"]  # Convert to boolean
