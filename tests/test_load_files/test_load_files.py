from warriorcats_translater.utils.config import load_config
from warriorcats_translater.utils.cache import diff_cache

print(load_config())

print(diff_cache({
    "A": {"C1": "content1", "C2": "content2"},
    "B": {"C1": "content1", "C2": "content2"}
    }))
