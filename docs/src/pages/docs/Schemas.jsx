export default function SchemasDoc() {
  return (
    <>
      <h1>Canonical Schemas</h1>
      <p><strong>File:</strong> <code>hermes/base.py</code></p>

      <h2>What They Do</h2>
      <p>
        All Hermes connectors normalize raw API responses into a single standard
        pandas DataFrame schema. This guarantees that any downstream consumer
        receives predictable column names, types, and formats.
      </p>

      <h2>Standard Indicator Schema</h2>
      <p>Every connector's <code>fetch()</code> output uses these columns:</p>
      <table>
        <thead>
          <tr><th>Column</th><th>Type</th><th>Example</th><th>Notes</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>date</code></td>
            <td><code>datetime64[ns]</code></td>
            <td><code>2024-01-01</code></td>
            <td>Always coerced via <code>pd.to_datetime</code></td>
          </tr>
          <tr>
            <td><code>country</code></td>
            <td><code>str</code></td>
            <td><code>"USA"</code></td>
            <td>ISO 3166-1 alpha-3, always uppercase</td>
          </tr>
          <tr>
            <td><code>indicator</code></td>
            <td><code>str</code></td>
            <td><code>"GDPC1"</code></td>
            <td>Series or indicator identifier</td>
          </tr>
          <tr>
            <td><code>value</code></td>
            <td><code>float64</code></td>
            <td><code>27366.0</code></td>
            <td>Coerced via <code>pd.to_numeric</code></td>
          </tr>
          <tr>
            <td><code>source</code></td>
            <td><code>str</code></td>
            <td><code>"fred"</code></td>
            <td>Lowercase connector name</td>
          </tr>
        </tbody>
      </table>

      <h2>Rules</h2>
      <ul>
        <li><code>date</code> is always <code>datetime64[ns]</code></li>
        <li><code>country</code> is always ISO 3166-1 alpha-3 uppercase</li>
        <li><code>value</code> is always <code>float64</code> (nulls coerce to NaN)</li>
        <li>Every DataFrame includes all 5 columns in order</li>
      </ul>

      <h2>Example Output</h2>
      <pre><code>{`# From hr.fred.fetch(country="USA", indicator="GDPC1")
# Columns:
#   date           datetime64[ns]  e.g. 2024-01-01
#   country        str             e.g. "USA"
#   indicator      str             e.g. "GDPC1"
#   value          float64         e.g. 27366.0
#   source         str             e.g. "fred"`}</code></pre>
    </>
  );
}
