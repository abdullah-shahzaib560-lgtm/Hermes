export default function WorldBankDoc() {
  return (
    <>
      <h1><code>World_bank</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/world_bank.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches indicator time series from the World Bank Indicators API — GDP, inflation,
        unemployment, governance, debt, and hundreds more. No authentication required.
      </p>
      <p><strong>API:</strong> <a href="https://api.worldbank.org/v2" target="_blank">api.worldbank.org/v2</a></p>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(opensanction_api=...)

# GDP growth (annual %)
df = hr.world_bank.fetch(
    country_code="USA",
    indicator_code="NY.GDP.MKTP.KD.ZG",
)`}</code></pre>

      <h3><code>fetch(country_code, indicator_code, frequency=None, most_recent=None, per_page=1000, page=1, force=False) → DataFrame</code></h3>
      <ul>
        <li><code>country_code</code> — ISO3 code, e.g. <code>"USA"</code></li>
        <li><code>indicator_code</code> — World Bank indicator ID, e.g. <code>"FP.CPI.TOTL.ZG"</code></li>
        <li><code>frequency</code> + <code>most_recent</code> — optional: request a specific frequency (<code>"Y"</code>/<code>"M"</code>/<code>"Q"</code>) with <code>mrv</code></li>
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
            <td>Observation period (e.g. <code>"2023"</code>)</td>
          </tr>
          <tr>
            <td><code>indicator_id</code></td>
            <td>Indicator code</td>
          </tr>
          <tr>
            <td><code>indicator_name</code></td>
            <td>Human-readable indicator name</td>
          </tr>
          <tr>
            <td><code>country</code></td>
            <td>ISO3 country code</td>
          </tr>
          <tr>
            <td><code>value</code></td>
            <td>The observation value</td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td>Always <code>"World_Bank"</code></td>
          </tr>
        </tbody>
      </table>

      <h2>Behavior</h2>
      <ul>
        <li>Responses are cached with a <strong>7-day TTL</strong>.</li>
        <li>Includes retry logic with exponential backoff on timeouts.</li>
        <li>Empty responses return a DataFrame with the standard columns.</li>
      </ul>
    </>
  );
}
