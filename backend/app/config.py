import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATASET_PATH: str = os.getenv("DATASET_PATH", "../datasets/raw/hvac_sensor_data.csv")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:19000,http://localhost:19006,exp://localhost:19000",
    ).split(",")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")


settings = Settings()
