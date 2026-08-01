export default function ExportDoc() {
  return (
    <>
      <h1>Data Export</h1>
      <p><strong>File:</strong> <code>hermes/core/export.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>export()</code> helper writes any <code>pandas.DataFrame</code> or
        <code>pandas.Series</code> to disk as CSV, JSON, or Parquet. It creates the target
        directory if it doesn't exist.
      </p>

      <h2>Signature</h2>
      <pre><code>{`export(
    data: pd.DataFrame | pd.Series,
    filetype: str = "csv",
    loc: Path | str = "data/",
    name: str | None = None,
)`}</code></pre>
      <table>
        <thead>
          <tr>
            <th>Argument</th>
            <th>Default</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>data</code></td>
            <td>—</td>
            <td>The DataFrame or Series to export.</td>
          </tr>
          <tr>
            <td><code>filetype</code></td>
            <td><code>"csv"</code></td>
            <td>One of <code>"csv"</code>, <code>"json"</code>, <code>"parquet"</code>.</td>
          </tr>
          <tr>
            <td><code>loc</code></td>
            <td><code>"data/"</code></td>
            <td>Target directory.</td>
          </tr>
          <tr>
            <td><code>name</code></td>
            <td><code>None</code></td>
            <td>Output filename (without extension). Defaults to a Unix timestamp.</td>
          </tr>
        </tbody>
      </table>

      <h2>Examples</h2>
      <pre><code>{`from hermes.core.export import export

# Save a country risk snapshot as JSON
export(data=risk, filetype="json", name="ukr_risk")

# Save a training panel as Parquet
export(data=panel, filetype="parquet", loc="data/panels/", name="monthly_panel")`}</code></pre>

      <blockquote>
        Passing anything other than a DataFrame or Series raises a <code>TypeError</code>.
        Unsupported file types are logged and skipped.
      </blockquote>
    </>
  );
}
