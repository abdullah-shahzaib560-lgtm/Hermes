export default function IMFDoc() {
  return (
    <>
      <h1><code>IMF</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/imf.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches time series from the IMF SDMX 3.0 API — International Financial Statistics
        (IFS), World Economic Outlook (WEO), Government Finance Statistics (GFS), and other
        dataflows. No authentication required.
      </p>
      <p><strong>API:</strong> <code>https://api.imf.org/external/sdmx/3.0/data/dataflow/</code></p>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(opensanction_api=...)

# GDP in national currency, IFS dataflow
df = hr.imf.fetch(
    country="USA",
    agency="IFS",
    dataflow_id="IFS",
    key="NGDP_R",
)`}</code></pre>

      <h3><code>fetch(country, agency, dataflow_id, key, force=False) → DataFrame</code></h3>
      <ul>
        <li><code>country</code> — ISO3 code, e.g. <code>"USA"</code> (converted to ISO2 internally)</li>
        <li><code>agency</code> — SDMX agency, e.g. <code>"IFS"</code>, <code>"WEO"</code></li>
        <li><code>dataflow_id</code> — dataflow, e.g. <code>"IFS"</code>, <code>"WEO"</code></li>
        <li><code>key</code> — indicator key within the dataflow, e.g. <code>"NGDP_R"</code></li>
        <li><code>force</code> — bypass the cache and refresh from the API</li>
      </ul>

      <h2>Output Columns</h2>
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>date</code></td>
            <td>Observation period</td>
          </tr>
          <tr>
            <td><code>indicator_id</code></td>
            <td>Indicator code (from the <code>INDICATOR</code>/<code>INDEX_TYPE</code> dimension)</td>
          </tr>
          <tr>
            <td><code>country</code></td>
            <td>Country code</td>
          </tr>
          <tr>
            <td><code>value</code></td>
            <td>The observation value</td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td>Always <code>"IMF"</code></td>
          </tr>
        </tbody>
      </table>
      <p>
        Any additional SDMX series dimensions (e.g. <code>FREQ</code>, <code>UNIT</code>) are
        appended as extra columns.
      </p>

      <h2>Behavior</h2>
      <ul>
        <li>Responses are cached with a <strong>7-day TTL</strong>.</li>
        <li>404s (unknown country/dataflow) return an empty DataFrame instead of raising.</li>
        <li>Includes retry logic with exponential backoff on timeouts.</li>
      </ul>
    </>
  );
}
