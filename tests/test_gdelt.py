from __future__ import annotations

import pandas as pd
import respx

from hermes.sources.gdelt import CANONICAL_COLUMNS, FIPS_TO_ISO3, GDELT, _classify_themes

GDELT_DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"


class TestClassifyThemes:
    def test_direct_match(self):
        assert _classify_themes(["PROTEST"]) == "protest"

    def test_semicolon_string(self):
        assert _classify_themes("CONFLICT;OTHER") == "conflict"

    def test_unknown(self):
        assert _classify_themes(["SOMETHING_WEIRD"]) == "unknown"

    def test_none(self):
        assert _classify_themes(None) == "unknown"


class TestFipsMapping:
    def test_fips_to_iso3(self):
        assert FIPS_TO_ISO3["US"] == "USA"
        assert FIPS_TO_ISO3["PK"] == "PAK"
        assert FIPS_TO_ISO3["AF"] == "AFG"

    def test_roundtrip(self):
        from hermes.sources.gdelt import ISO3_TO_FIPS

        assert ISO3_TO_FIPS["USA"] == "US"


class TestToCanonical:
    def test_empty(self):
        gdelt = GDELT(cache=None)
        df = pd.DataFrame()
        result = gdelt._to_canonical(df)
        assert list(result.columns) == CANONICAL_COLUMNS
        assert result.empty

    def test_with_url_and_date_and_fips(self):
        gdelt = GDELT(cache=None)
        df = pd.DataFrame(
            {
                "url": ["http://example.com/1"],
                "seendate": ["20240301120000"],
                "ActionGeo_CountryCode": ["US"],
                "themes": [["PROTEST"]],
                "tone": [-2.5],
                "ActionGeo_Lat": [38.0],
                "ActionGeo_Long": [-97.0],
            }
        )
        result = gdelt._to_canonical(df)
        assert not result.empty
        assert result["event_id"].iloc[0] == "http://example.com/1"
        assert result["country_iso3"].iloc[0] == "USA"
        assert result["event_type"].iloc[0] == "protest"
        assert result["severity"].iloc[0] == -2.5
        assert result["lat"].iloc[0] == 38.0
        assert result["lon"].iloc[0] == -97.0
        assert result["source"].iloc[0] == "gdelt"

    def test_event_root_code_classification(self):
        gdelt = GDELT(cache=None)
        df = pd.DataFrame(
            {
                "url": ["http://ex.com"],
                "SQLDATE": ["20240301"],
                "ActionGeo_CountryCode": ["US"],
                "EventRootCode": ["14"],
                "GoldsteinScale": [5.0],
                "ActionGeo_Lat": [0.0],
                "ActionGeo_Long": [0.0],
            }
        )
        result = gdelt._to_canonical(df)
        assert result["event_type"].iloc[0] == "protest"

    def test_drops_rows_without_date(self):
        gdelt = GDELT(cache=None)
        df = pd.DataFrame(
            {
                "url": ["http://a", "http://b"],
                "SQLDATE": ["20240301", pd.NA],
                "ActionGeo_CountryCode": ["US", "US"],
            }
        )
        result = gdelt._to_canonical(df)
        assert len(result) == 1


class TestGDELTQuery:
    @respx.mock
    def test_query_events_cache_hit(self, tmp_cache):
        gdelt = GDELT(cache=tmp_cache)
        respx.get(GDELT_DOC_API).respond(
            status_code=200,
            json={"articles": [{"url": "http://x", "seendate": "20240301000000", "themes": ["PROTEST"]}]},
        )
        df1 = gdelt.query_events(themes=["PROTEST"])
        df2 = gdelt.query_events(themes=["PROTEST"])
        assert len(respx.calls) == 1

    @respx.mock
    def test_query_events_no_articles(self, tmp_cache):
        gdelt = GDELT(cache=tmp_cache)
        respx.get(GDELT_DOC_API).respond(
            status_code=200,
            json={"articles": []},
        )
        df = gdelt.query_events(themes=["PROTEST"])
        assert df.empty
