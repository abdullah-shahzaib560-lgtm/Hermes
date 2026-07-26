import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable


class TieredPlan:
    def __init__(self, tiers: list[list[str]], all_features: list[str]):
        self.tiers = tiers
        self.all_features = all_features


class LineageGraph:
    def __init__(self):
        self.features: dict[str, dict[str, Any]] = {}
        self.groups: dict[str, list[str]] = {}

    def register_feature(
        self,
        name: str,
        group: str,
        deps: list[str],
        compute: str,
        fn: Callable,
    ):
        self.features[name] = {
            "group": group,
            "deps": deps,
            "compute": compute,
            "function": fn,
        }
        if group not in self.groups:
            self.groups[group] = []
        if name not in self.groups[group]:
            self.groups[group].append(name)

    def get_feature(self, name: str) -> dict[str, Any] | None:
        return self.features.get(name)

    def get_group_features(self, group: str) -> list[str]:
        return self.groups.get(group, [])

    def resolve_group(self, group: str) -> TieredPlan:
        feature_names = self.groups.get(group, [])
        if not feature_names:
            return TieredPlan([], [])

        remaining = set(feature_names)
        tiers: list[list[str]] = []

        while remaining:
            tier: list[str] = []
            for name in list(remaining):
                feat = self.features[name]
                feature_deps = {d for d in feat["deps"] if d in self.features}
                cross_feature_deps = feature_deps & remaining
                cross_feature_deps.discard(name)
                if not cross_feature_deps:
                    tier.append(name)
            if not tier:
                tier = list(remaining)[:1]
            for name in tier:
                remaining.discard(name)
            tiers.append(tier)

        return TieredPlan(tiers, feature_names)

    def save(self, path: str | Path):
        data = {
            "features": {
                name: {
                    "group": info["group"],
                    "deps": info["deps"],
                    "compute": info["compute"],
                }
                for name, info in self.features.items()
            },
            "groups": dict(self.groups),
        }
        Path(path).write_text(json.dumps(data, indent=2))

    def load(self, path: str | Path):
        data = json.loads(Path(path).read_text())
        self.features = {}
        self.groups = data.get("groups", {})
        for name, info in data.get("features", {}).items():
            self.features[name] = {
                "group": info["group"],
                "deps": info["deps"],
                "compute": info["compute"],
                "function": None,
            }


lineagegraph = LineageGraph()


def feature(
    name: str,
    group: str,
    deps: list[str],
    compute: str,
):
    def decorator(func: Callable):
        lineagegraph.register_feature(
            name=name,
            group=group,
            deps=deps,
            compute=compute,
            fn=func,
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
