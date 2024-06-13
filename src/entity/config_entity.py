import os,sys
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestonConfig:
    dir:Path
    raw_data: Path
    train_data:Path
    test_data:Path
    