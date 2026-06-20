from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SENDGRID_API_KEY: str = ""
    ALLOWED_ORIGINS_STR: str = Field(
        default="http://localhost:5173,http://localhost:4173",
        alias="ALLOWED_ORIGINS",
    )
    WIDGET_SECRET: str = ""
    JWT_SECRET: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_STR.split(",")]


settings = Settings()
