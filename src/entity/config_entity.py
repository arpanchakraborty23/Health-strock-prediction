import os,sys
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestonConfig:
    dir:Path
    raw_data: Path
    train_data:Path
    test_data:Path
    
@dataclass
class DatatranformationConfig:
    dir: Path
    train_arr:Path
    test_arr: Path
    target_col:Path
    train_data:Path
    test_data:Path
    preprocess_obj:Path