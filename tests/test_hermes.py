from __future__ import annotations

from unittest.mock import patch

from hermes import Hermes


class TestHermes:
    def test_init(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
        )
        assert hermes.country_features is not None
        assert hermes.gdelt is not None
        assert hermes.imf is not None
        assert hermes.opensanction is not None
        assert hermes.world_bank is not None
        assert hermes.fred is not None
        assert hermes.binance is not None
        assert hermes.sec_edger is not None
        assert hermes.finnhub is not None
        assert hermes.yfin is not None
        assert hermes.datasets is not None
        assert hermes.ta_feature is not None
        assert hermes.fa_features is not None
        assert hermes._cache is not None

    def test_init_no_cache(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
            use_cache=False,
        )
        assert hermes._cache is None

    @patch("hermes.Hermes.clear_cache")
    def test_clear_cache_dispatches(self, mock_clear):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
        )
        hermes.clear_cache(older_than="7d")
        mock_clear.assert_called_once_with(older_than="7d")

    def test_cache_stats_without_cache(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
            use_cache=False,
        )
        stats = hermes.cache_stats()
        assert stats["total_files"] == 0

    def test_cache_stats_with_cache(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
        )
        stats = hermes.cache_stats()
        assert isinstance(stats, dict)
        assert "total_files" in stats

    def test_list_countries(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
        )
        assert isinstance(hermes.list_countries, list)
        assert len(hermes.list_countries) > 0
        assert "USA" in hermes.list_countries

    def test_list_features(self):
        hermes = Hermes(
            opensanction_api="test-key",
            new_data_api="",
            fred_api="test-fred",
            sec_username="test-sec-user",
            sec_email="test-sec-email",
            finnhub_api="test-finnhub",
        )
        assert isinstance(hermes.list_features, list)
        assert len(hermes.list_features) > 0
