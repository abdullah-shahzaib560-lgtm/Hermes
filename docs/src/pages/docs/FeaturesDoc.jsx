export default function FeaturesDoc() {
  return (
    <>
      <h1>Features Pipeline</h1>
      <p><strong>Module:</strong> <code>hermes/features/</code></p>

      <h2>What It Does</h2>
      <p>
        The features pipeline pulls raw data from all connectors and engineers
        derived risk indicators: YoY growth rates, rolling volatility, trend
        classification, regime type detection, and composite scores.
      </p>

      <h2>Key Functions</h2>

      <h3><code>get_country_risk_features()</code></h3>
      <pre><code>{`from hermes.features import get_country_risk_features

risk = get_country_risk_features(
    country="UKR",
    date="2024-06-30",
    connectors=h.connectors,
)

print(risk["gdp_growth_yoy"])
print(risk["inflation_cpi_yoy"])
print(risk["unemployment_rate"])
print(risk["regime_classification"])
print(risk["trend_classification"])`}</code></pre>

      <p>Returns a dict with 35+ fields covering:</p>
      <ul>
        <li><strong>Economic:</strong> GDP growth, inflation, unemployment, industrial production, PPI</li>
        <li><strong>External:</strong> Current account, FX reserves, external debt</li>
        <li><strong>Fiscal:</strong> Deficit-to-GDP, government debt-to-GDP</li>
        <li><strong>Financial:</strong> Credit spreads, yield curve, banking sector health</li>
        <li><strong>Governance:</strong> Regime classification, governance effectiveness, corruption control</li>
        <li><strong>Security:</strong> Goldstein violence score, civil unrest risk, news sentiment</li>
      </ul>

      <h3><code>get_timeseries()</code></h3>
      <pre><code>{`from hermes.features import get_timeseries

ts = get_timeseries(
    connectors=h.connectors,
    country="USA",
    indicator="gdp_growth_yoy",
    start="2020-01-01",
    end="2024-12-31",
)   # -> [{"date": ..., "value": ...}]`}</code></pre>

      <h3><code>list_available()</code></h3>
      <pre><code>{`from hermes.features import list_available

for f in list_available():
    print(f["name"], f["category"], f["description"])`}</code></pre>

      <table>
        <thead><tr><th>Feature</th><th>Category</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td><code>gdp_growth_yoy</code></td><td>economic</td><td>GDP year-over-year growth rate</td></tr>
          <tr><td><code>inflation_cpi_yoy</code></td><td>economic</td><td>CPI inflation YoY</td></tr>
          <tr><td><code>unemployment_rate</code></td><td>economic</td><td>Unemployment rate</td></tr>
          <tr><td><code>regime_classification</code></td><td>governance</td><td>democracy/hybrid/autocracy</td></tr>
          <tr><td><code>goldstein_score_violence</code></td><td>security</td><td>Goldstein violence score (0-1)</td></tr>
          <tr><td><code>news_sentiment_7d</code></td><td>sentiment</td><td>7-day avg news sentiment (-1 to 1)</td></tr>
        </tbody>
      </table>
    </>
  );
}
