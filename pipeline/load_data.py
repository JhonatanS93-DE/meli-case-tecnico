import pandas as pd

def load_jsonl(file_path):
    """Load JSON Lines file using pandas"""
    return pd.read_json(file_path, lines=True)

def load_all_sources():
    """Load all required data sources and return as dict"""
    prints = load_jsonl("data/input/prints.json")
    taps = load_jsonl("data/input/taps.json")
    pays = pd.read_csv("data/input/pays.csv")
    return {"prints": prints, "taps": taps, "pays": pays}
