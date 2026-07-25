export default function VDemDoc() {
  return (
    <>
      <h1>V-Dem Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/v_dem.py</code></p>
      <p><strong>Class:</strong> <code>VDem(BaseConnector)</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches democracy indices and governance quality metrics from the
        Varieties of Democracy (V-Dem) project. Provides regime classifications,
        civil liberties scores, and institutional quality indicators.
      </p>

      <h2>Key Methods</h2>
      <pre><code>{`fetch(country="", indicator="democracy_index") -> pd.DataFrame`}</code></pre>
      <p>
        Supports indicators: <code>democracy_index</code>, <code>liberal_democracy</code>,
        <code>participatory_democracy</code>, <code>civil_liberties</code>
      </p>

      <h2>Available Countries</h2>
      <p>USA, GBR, DEU, FRA, JPN, CHN, IND, BRA, RUS, ZAF, UKR, MEX, IRN</p>

      <h2>Date Range</h2>
      <p>1900-01-01 to present</p>
    </>
  );
}
