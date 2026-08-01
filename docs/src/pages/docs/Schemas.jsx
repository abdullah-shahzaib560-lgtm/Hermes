export default function SchemasDoc() {
  return (
    <>
      <h1>Canonical Schemas</h1>

      <h2>Connector Output</h2>
      <p>
        Every indicator-based connector (World Bank, IMF) returns the same core shape, so
        feature functions can rely on a stable contract:
      </p>
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Example</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>date</code></td>
            <td>string</td>
            <td><code>"2023"</code></td>
          </tr>
          <tr>
            <td><code>indicator_id</code></td>
            <td>string</td>
            <td><code>"NY.GDP.MKTP.KD.ZG"</code></td>
          </tr>
          <tr>
            <td><code>country</code></td>
            <td>string</td>
            <td><code>"USA"</code></td>
          </tr>
          <tr>
            <td><code>value</code></td>
            <td>float</td>
            <td><code>2.1</code></td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td>string</td>
            <td><code>"World_Bank"</code> / <code>"IMF"</code></td>
          </tr>
        </tbody>
      </table>

      <h2>GDELT Event Schema</h2>
      <p>
        Event-based connectors (GDELT) normalize to a different schema — one row per event,
        with no fixed frequency:
      </p>
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>event_id</code></td>
            <td>string</td>
            <td>Global event ID</td>
          </tr>
          <tr>
            <td><code>date</code></td>
            <td>datetime</td>
            <td>Event timestamp</td>
          </tr>
          <tr>
            <td><code>country_iso3</code></td>
            <td>string</td>
            <td>ISO3 country code</td>
          </tr>
          <tr>
            <td><code>event_type</code></td>
            <td>string</td>
            <td>protest / conflict / diplomacy / sanction / ...</td>
          </tr>
          <tr>
            <td><code>severity</code></td>
            <td>float</td>
            <td>Tone or Goldstein scale</td>
          </tr>
          <tr>
            <td><code>lat</code>, <code>lon</code></td>
            <td>float</td>
            <td>Coordinates</td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td>string</td>
            <td>Always <code>"gdelt"</code></td>
          </tr>
        </tbody>
      </table>

      <h2>Feature Output</h2>
      <p>Feature functions return one of two shapes, selected by the <code>mode</code> argument:</p>
      <ul>
        <li><code>mode="F"</code> — a single <code>float</code> / <code>int</code> (latest snapshot), or <code>NaN</code> when no data exists</li>
        <li><code>mode="ML"</code> — a <code>pd.Series</code> indexed monthly, empty when no data exists</li>
      </ul>

      <h2>Risk Snapshot Schema</h2>
      <p><code>get_country_risk_features()</code> returns a nested dict:</p>
      <pre><code>{`{
    "country": "UKR",
    "economic":     { "gdp_growth_yoy": 3.2, ... },
    "geopolitical": { "conflict_event_count_30d": 47, ... },
    "security":     { "military_spending_gdp": 4.1, ... },
    "social":       { "human_development_index": 0.73, ... },
    "environmental":{ "climate_vulnerability_score": 0.62, ... },
    "metadata":     { "last_updated": "...", "features_version": "1.0.0" },
}`}</code></pre>

      <h2>Training Panel Schema</h2>
      <p><code>build_training_panel()</code> returns a DataFrame with a <code>(country_iso3, date)</code> MultiIndex and one column per feature.</p>
    </>
  );
}
