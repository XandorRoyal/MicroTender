from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    # Application Settings
    PROTOCOL: str
    BASE_URL: str
    PORT: int
    HOT_RELOAD: bool = False

    # Discord Connection Settings
    APP_ID: str
    APP_SECRET: str
    AUTHENTICATION_ENDPOINT: str = "/auth/authenticate"

    # Minecraft Verification Settings
    MC_COORDINATES: str
    MC_VERIFY_URL: str

    # Database Settings
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_MAX_POOL_SIZE: int = 10
    DB_MIN_POOL_SIZE: int = 9

    model_config = SettingsConfigDict(env_file=".env")

# Use a single instance of Settings throughout the application
settings_instance = None
def get_settings():
    global settings_instance
    if settings_instance is None:
        settings_instance = Settings()
    return settings_instance