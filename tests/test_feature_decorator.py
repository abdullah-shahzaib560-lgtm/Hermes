from __future__ import annotations

import tempfile
from pathlib import Path

from hermes.features.decorator import LineageGraph, TieredPlan, feature, lineagegraph


class TestTieredPlan:
    def test_init(self):
        plan = TieredPlan([["a"], ["b"]], ["a", "b"])
        assert plan.tiers == [["a"], ["b"]]
        assert plan.all_features == ["a", "b"]


class TestLineageGraph:
    def test_register_and_get(self):
        g = LineageGraph()

        def dummy():
            pass

        g.register_feature("f1", "g1", ["dep1"], "compute1", dummy)
        feat = g.get_feature("f1")
        assert feat is not None
        assert feat["group"] == "g1"
        assert feat["deps"] == ["dep1"]
        assert feat["compute"] == "compute1"
        assert feat["function"] is dummy

    def test_get_feature_nonexistent(self):
        g = LineageGraph()
        assert g.get_feature("nope") is None

    def test_get_group_features(self):
        g = LineageGraph()
        g.register_feature("a", "g1", [], "", lambda: None)
        g.register_feature("b", "g1", [], "", lambda: None)
        assert g.get_group_features("g1") == ["a", "b"]

    def test_get_group_features_empty(self):
        g = LineageGraph()
        assert g.get_group_features("nonexistent") == []

    def test_resolve_group_no_deps(self):
        g = LineageGraph()
        g.register_feature("a", "g1", [], "", lambda: None)
        g.register_feature("b", "g1", [], "", lambda: None)
        plan = g.resolve_group("g1")
        assert len(plan.tiers) == 1
        assert set(plan.tiers[0]) == {"a", "b"}

    def test_resolve_group_with_deps(self):
        g = LineageGraph()
        g.register_feature("a", "g1", [], "", lambda: None)
        g.register_feature("b", "g1", ["a"], "", lambda: None)
        g.register_feature("c", "g1", ["b"], "", lambda: None)
        plan = g.resolve_group("g1")
        assert len(plan.tiers) == 3
        assert plan.tiers[0] == ["a"]
        assert plan.tiers[1] == ["b"]
        assert plan.tiers[2] == ["c"]

    def test_resolve_group_unknown(self):
        g = LineageGraph()
        plan = g.resolve_group("ghost")
        assert plan.tiers == []
        assert plan.all_features == []

    def test_save_load_roundtrip(self):
        g = LineageGraph()
        g.register_feature("x", "g1", ["y"], "some_fn", lambda: None)
        g.register_feature("y", "g1", [], "other_fn", lambda: None)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
            g.save(path)

        g2 = LineageGraph()
        g2.load(path)
        Path(path).unlink()

        assert g2.get_feature("x") is not None
        assert g2.get_feature("x")["group"] == "g1"
        assert g2.get_feature("x")["deps"] == ["y"]
        assert g2.get_feature("x")["function"] is None
        assert g2.get_group_features("g1") == ["x", "y"]


class TestFeatureDecorator:
    def test_decorator_registers(self):
        @feature(name="test_feat", group="test_group", deps=[], compute="test")
        def my_fn():
            return 42

        feat = lineagegraph.get_feature("test_feat")
        assert feat is not None
        assert feat["group"] == "test_group"
        assert feat["compute"] == "test"

    def test_decorator_wrapper_works(self):
        @feature(name="wrapper_test", group="wg", deps=[], compute="")
        def add(a, b):
            return a + b

        assert add(3, 4) == 7
