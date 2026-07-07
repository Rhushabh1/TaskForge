from dotenv import load_dotenv
import os


load_dotenv()


class Settings:

	DATABASE_URL = {
		f"postgresql://"
		f"{os.getenv("POSTGRES_USER")}:"
		f"{os.getenv("POSTGRES_PASSWORD")}@"
		f"{os.getenv("POSTGRES_HOST")}:"
		f"{os.getenv("POSTGRES_PORT")}/"
		f"{os.getenv("POSTGRES_DB")}"
	}


settings = Settings()