from __future__ import annotations

from unittest.mock import patch

from hermes import Hermes


class TestHermes:
    def test_init(self):
        hermes = Hermes(opensanction_api="test-key", new_data_api="")
        assert hermes.features is not None
        assert hermes.gdelt is not None
        assert hermes.imf is not None
        assert hermes.opensanction is not None
        assert hermes.world_bank is not None
        assert hermes._cache is not None

    def test_init_no_cache(self):
        hermes = Hermes(opensanction_api="test-key", new_data_api="", use_cache=False)
        assert hermes._cache is None

    @patch("hermes.Hermes.clear_cache")
    def test_clear_cache_dispatches(self, mock_clear):
        hermes = Hermes(opensanction_api="test-key", new_data_api="")
        hermes.clear_cache(older_than="7d")
        mock_clear.assert_called_once_with(older_than="7d")

    def test_cache_stats_without_cache(self):
        hermes = Hermes(opensanction_api="test-key", new_data_api="", use_cache=False)
        stats = hermes.cache_stats()
        assert stats["total_files"] == 0

    def test_cache_stats_with_cache(self):
        hermes = Hermes(opensanction_api="test-key", new_data_api="")
        stats = hermes.cache_stats()
        assert isinstance(stats, dict)
        assert "total_files" in stats
