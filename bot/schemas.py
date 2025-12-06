from dataclasses import dataclass

from bot.enums import WhenPair


@dataclass
class AddingSkipStateSchema:
    when_pair: WhenPair
    pair_number: int
    subject_name: str
    reason: str
