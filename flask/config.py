from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from repository root so values are available in os.environ
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
	load_dotenv(dotenv_path=env_path)

OS2_API_BASE_URL = os.environ.get("OS2_IOT_API_BASE_URL", "https://os2iot-backend.prod.os2iot.kmd.dk/api/v1/")
OS2_API_KEY = os.environ.get("OS2_API_KEY")  # Required
OS2_APPLICATION_ID = int(os.environ.get("OS2_APPLICATION_ID"))  # Required
OS2_DEVICE_PROFILE_ID = os.environ.get("OS2_DEVICE_PROFILE_ID")  # Required
OS2_VERIFY = os.environ.get("OS2_VERIFY", "True") in ["True", "true", "1"]  # Convert to boolean
