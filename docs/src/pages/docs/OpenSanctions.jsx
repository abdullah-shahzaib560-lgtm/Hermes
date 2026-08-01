export default function OpenSanctionsDoc() {
  return (
    <>
      <h1><code>OpenSanction</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/opensanctions.py</code></p>

      <h2>What It Does</h2>
      <p>
        Queries the <a href="https://www.opensanctions.org/" target="_blank">OpenSanctions</a>{' '}
        API for individuals and entities on sanctions lists, by country. Requires an API key
        (passed to the <code>Hermes</code> constructor or as an env var).
      </p>
      <p><strong>API:</strong> <code>https://api.opensanctions.org</code></p>

      <h2>Datasets</h2>
      <p>Common datasets you can pass to <code>fetch()</code>:</p>
      <table>
        <thead>
          <tr>
            <th>Dataset</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>us_ofac_sdn</code></td>
            <td>US OFAC Specially Designated Nationals</td>
          </tr>
          <tr>
            <td><code>eu_fsf</code></td>
            <td>EU Financial Sanctions Files</td>
          </tr>
          <tr>
            <td><code>uk_fcdos</code></td>
            <td>UK FCDO Sanctions List</td>
          </tr>
          <tr>
            <td><code>un_sc</code></td>
            <td>UN Security Council Sanctions</td>
          </tr>
        </tbody>
      </table>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(opensanction_api=os.getenv("OPEN_SANCTIONS_API"))

# US OFAC list entries linked to Russia
data = hr.opensanction.fetch(
    country="RUS",
    dataset="us_ofac_sdn",
    limit=50,
)`}</code></pre>

      <h3><code>fetch(country, dataset, limit=50, changed_since=None, topic=None, facets=None, force=False) → DataFrame</code></h3>
      <ul>
        <li><code>country</code> — ISO3 code (converted to ISO2 internally)</li>
        <li><code>dataset</code> — one of the datasets above (required; empty raises <code>ValueError</code>)</li>
        <li><code>limit</code> — max results, capped at 1000</li>
        <li><code>changed_since</code> — ISO date to only fetch entities changed after it</li>
        <li><code>topic</code> — filter by sanctions topic</li>
        <li><code>facets</code> — request response facets</li>
        <li><code>force</code> — bypass the cache</li>
      </ul>

      <h2>Behavior</h2>
      <ul>
        <li>Responses are cached with a <strong>30-day TTL</strong>.</li>
        <li>Retries with exponential backoff on timeouts and 5xx errors.</li>
        <li>404 (unknown dataset) or invalid country codes return an empty result.</li>
      </ul>
    </>
  );
}
