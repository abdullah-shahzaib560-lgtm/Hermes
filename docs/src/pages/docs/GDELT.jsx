export default function GDELTDoc() {
  return (
    <>
      <h1><code>GDELT</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/gdelt.py</code></p>

      <h2>What It Does</h2>
      <p>
        Queries the <a href="https://www.gdeltproject.org/" target="_blank">GDELT</a> global
        event database — conflict, protest, diplomacy, and sanctions events extracted from news
        worldwide. No authentication required.
      </p>
      <p>
        Supports two fetch paths: the <strong>Doc API</strong> (lightweight article queries by
        country and theme) and <strong>daily exports</strong> (full event files, used internally
        for ML mode history).
      </p>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes
from datetime import datetime, timedelta

hr = Hermes(opensanction_api=...)

# Conflict events for Ukraine over the last 30 days
events = hr.gdelt.query_events(
    countries=["UKR"],
    themes=["CONFLICT"],
    start_date=datetime.utcnow() - timedelta(days=30),
    end_date=datetime.utcnow(),
)`}</code></pre>

      <h3><code>query_events(countries=None, themes=None, start_date=None, end_date=None, normalize=True, force=False) → DataFrame</code></h3>
      <ul>
        <li><code>countries</code> — list of ISO3 codes (converted to FIPS internally)</li>
        <li><code>themes</code> — event themes; each maps to GKG theme codes:
          <table>
            <thead>
              <tr>
                <th>Theme</th>
                <th>Mapped GKG themes</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>"PROTEST"</code></td>
                <td>PROTEST, Riot, RiotProtect, ...</td>
              </tr>
              <tr>
                <td><code>"CONFLICT"</code></td>
                <td>CONFLICT, Military, Assault, Fight, ...</td>
              </tr>
              <tr>
                <td><code>"DIPLOMACY"</code></td>
                <td>DIPLOMACY, Agree, Endorse, ...</td>
              </tr>
              <tr>
                <td><code>"SANCTIONS"</code></td>
                <td>Sanction, Embargo</td>
              </tr>
            </tbody>
          </table>
        </li>
        <li><code>start_date</code> / <code>end_date</code> — datetime bounds</li>
        <li><code>normalize</code> — map to the canonical event schema (default <code>True</code>)</li>
        <li><code>force</code> — bypass the cache</li>
      </ul>

      <h2>Canonical Output Columns</h2>
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>event_id</code></td>
            <td>Global event ID</td>
          </tr>
          <tr>
            <td><code>date</code></td>
            <td>Event timestamp</td>
          </tr>
          <tr>
            <td><code>country_iso3</code></td>
            <td>ISO3 country code (from FIPS)</td>
          </tr>
          <tr>
            <td><code>event_type</code></td>
            <td>Classified type: protest / conflict / diplomacy / sanction / ...</td>
          </tr>
          <tr>
            <td><code>severity</code></td>
            <td>Tone or Goldstein scale value</td>
          </tr>
          <tr>
            <td><code>lat</code> / <code>lon</code></td>
            <td>Event coordinates</td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td>Always <code>"gdelt"</code></td>
          </tr>
        </tbody>
      </table>

      <h2>Behavior</h2>
      <ul>
        <li>Responses are cached with a <strong>6-hour TTL</strong>.</li>
        <li>When <code>normalize=False</code>, raw Doc API / export columns are returned.</li>
        <li>Export downloads are capped in file count and parallelized with a thread pool.</li>
      </ul>
    </>
  );
}
