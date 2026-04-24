from dataclasses import dataclass
from typing import Optional, Tuple


class MazeConfig(dataclass):
    width: int
    height: int
    entry_x: int
    entry_y: int
    exit_x: int
    exit_y: int
    output_file: str
    perfect: bool

    seed: Optional[int] = None
    algorithm: Optional[str] = None
    display: Optional[str] = None

def parse_config(config_txt) -> MazeConfig:
    print(config_txt)
    try:
        # archivo = with open(config_txt)
        for line in f:
            pass
    except:
        pass
    
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for r in required:
        for rr in archivo:
            width = rr[r]
    
    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=data['OUTPUT_FILE'],
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
        display=display
    )
    

