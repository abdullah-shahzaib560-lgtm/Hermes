from functools import wraps
import inspect
from typing import Callable, Any, Dict, List

class LineageGraph:

    def __init__(self):
        self.feature: Dict[str, Dict[str, Any]] = {}
        self.group: Dict[str, List[str]] = {}

    def register_feature(
        self,
        name: str,
        group: str,
        deps: list[str],
        compute: str,
        fn: Callable
    ):
        self.feature[name] = {
            'group': group,
            'deps': deps,
            'compute': compute,
            'function': fn
        }

        if group not in self.group:
            self.group[group] = []
        if name not in self.group[group]:
            self.group[group].append(name)

lineagegraph = LineageGraph()

def feature(
    name: str,
    group: str,
    deps: list[str],
    compute: str
):
    def decorator(func: Callable):
        lineagegraph.register_feature(
            name=name,
            group=group,
            deps=deps,
            compute=compute,
            fn=func
        )
        @wraps
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
