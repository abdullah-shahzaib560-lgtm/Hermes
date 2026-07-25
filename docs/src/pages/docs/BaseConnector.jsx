export default function BaseConnectorDoc() {
  return (
    <>
      <h1><code>BaseConnector</code></h1>
      <p><strong>File:</strong> <code>hermes/base.py</code></p>

      <h2>What It Does</h2>
      <p>
        <code>BaseConnector</code> is the abstract base class for all Hermes connectors.
        Every connector must implement its interface, guaranteeing standardized output
        across all data sources.
      </p>

      <h2>Standard Output Schema</h2>
      <pre><code>{`STD_COLUMNS = ["date", "country", "indicator", "value", "source"]`}</code></pre>
      <table>
        <thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td><code>date</code></td><td><code>datetime64[ns]</code></td><td>Observation date</td></tr>
          <tr><td><code>country</code></td><td><code>str</code></td><td>ISO 3166-1 alpha-3 uppercase</td></tr>
          <tr><td><code>indicator</code></td><td><code>str</code></td><td>Series or indicator identifier</td></tr>
          <tr><td><code>value</code></td><td><code>float64</code></td><td>Numeric observation value</td></tr>
          <tr><td><code>source</code></td><td><code>str</code></td><td>Connector source name</td></tr>
        </tbody>
      </table>

      <h2>Methods to Implement</h2>
      <pre><code>{`fetch(self, **kwargs) -> pd.DataFrame
normalize(self, df, **kwargs) -> pd.DataFrame
validate(self, df) -> bool
get_available_countries(self) -> list[str]
get_date_range(self, country) -> tuple[str, str]`}</code></pre>
      <p>
        <code>fetch()</code> is the primary method — it retrieves data and returns a
        DataFrame with the standard schema. <code>normalize()</code> calls
        <code>ensure_std_schema()</code> to verify column presence and correct types.
      </p>

      <h2>Utility Function</h2>
      <pre><code>{`ensure_std_schema(df, source_name) -> pd.DataFrame`}</code></pre>
      <p>
        Validates that the DataFrame has all required columns, casts types to the
        standard dtypes, sorts by date, and assigns the source name.
      </p>
    </>
  );
}
