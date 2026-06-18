from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SENDGRID_API_KEY: str = ""
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:4173"]
    WIDGET_SECRET: str = ""
    JWT_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env")

    def model_post_init(self, __context):
        # Allow ALLOWED_ORIGINS to be provided as a comma-separated string
        if isinstance(self.ALLOWED_ORIGINS, str):
            object.__setattr__(self, "ALLOWED_ORIGINS", [o.strip() for o in self.ALLOWED_ORIGINS.split(",")])


settings = Settings()
