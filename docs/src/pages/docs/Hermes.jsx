export default function HermesDoc() {
  return (
    <>
      <h1><code>Hermes</code> Class</h1>
      <p><strong>File:</strong> <code>hermes/__init__.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>Hermes</code> class is the top-level entry point for the Hermes SDK.
        It composes all connectors, cache, and feature pipeline into a single unified interface.
      </p>

      <h2>Constructor</h2>
      <pre><code>{`Hermes(api_keys: dict[str, str] | None = None,
       cache_dir: str | Path | None = None)`}</code></pre>
      <ul>
        <li><strong>api_keys</strong> — Optional dict mapping connector names to API keys (e.g. <code>{'{'}&quot;fred&quot;: &quot;abc123&quot;{'}'}</code>)</li>
        <li><strong>cache_dir</strong> — Optional path for Parquet data cache (defaults to <code>~/.hermes_cache</code>)</li>
      </ul>

      <h2>Properties</h2>
      <ul>
        <li><code>.fred</code> — FRED economic data connector</li>
        <li><code>.world_bank</code> — World Bank data connector</li>
        <li><code>.bis</code> — Bank for International Settlements connector</li>
        <li><code>.imf</code> — IMF DataMapper connector</li>
        <li><code>.gdelt</code> — GDELT event data connector</li>
        <li><code>.ucdp</code> — Uppsala Conflict Data connector</li>
        <li><code>.newsapi</code> — NewsAPI connector</li>
        <li><code>.v_dem</code> — V-Dem democracy indices connector</li>
        <li><code>.comtrade</code> — UN Comtrade trade data connector</li>
        <li><code>.connectors</code> — Dict mapping name → connector instance</li>
      </ul>

      <h2>Key Methods</h2>
      <pre><code>{`# List all available connectors
hr.list_connectors() -> [{"name": ..., "type": ...}]

# Get comprehensive risk features for a country
hr.get_country_risk_features(
    country: str,
    date: str | None = None,
    features: list[str] | None = None,
) -> dict[str, Any]

# Get time series for a specific indicator
hr.get_timeseries(
    country: str,
    indicator: str,
    start: str = "",
    end: str = "",
) -> list[dict]`}</code></pre>

      <h2>Usage Example</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(api_keys={"fred": "..."})

# Get all risk features
risk = hr.get_country_risk_features("UKR", "2024-06-30")
print(risk["gdp_growth_yoy"])
print(risk["regime_classification"])
print(risk["goldstein_score_violence"])`}</code></pre>
    </>
  );
}
