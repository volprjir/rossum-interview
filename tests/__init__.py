import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), 'test_data', '.env.test')
load_dotenv(env_path)
