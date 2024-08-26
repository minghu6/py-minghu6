

from typing import List, Any

################################################################################
### Side Effect Function

def do_resize(l: List[Any], sz: int, val: Any) -> List[int]:
    if len(l) <= sz:
        return l[0:sz]
    else:
        l.extend([val] * (sz - len(l)))

