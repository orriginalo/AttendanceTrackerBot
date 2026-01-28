from dataclasses import dataclass, field
import os
from dotenv import load_dotenv


load_dotenv(override=True)


@dataclass
class ProjectSettings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    OWNER_ID: int = int(os.getenv("OWNER_ID"))
    DB_FILENAME: str = os.getenv("DB_FILENAME")

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///./data/{self.DB_FILENAME}"

    PAIR_TIMES: dict = field(
        default_factory=lambda: {
            1: "8:30 - 9:50",
            2: "10:00 - 11:20",
            3: "11:30 - 12:50",
            4: "13:30 - 14:50",
            5: "15:00 - 16:20",
            6: "16:30 - 17:50",
            7: "18:00 - 19:20",
            8: "19:30 - 20:50",
        }
    )

    REASONS: list = field(default_factory=lambda: ["Болел", "Впадлу", "Дела"])


settings: ProjectSettings = ProjectSettings()
