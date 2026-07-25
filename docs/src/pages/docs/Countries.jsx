export default function CountriesDoc() {
  return (
    <>
      <h1><code>Countries</code></h1>
      <p><strong>File:</strong> <code>hermes/countries.py</code></p>

      <h2>What It Does</h2>
      <p>
        Provides static country metadata: ISO codes, regions, income groups,
        capitals, currencies, and neighbor relationships.
      </p>

      <h2>Key Functions</h2>
      <pre><code>{`get_country_metadata(country) -> dict | None
list_countries() -> list[dict]
get_region(country) -> str
get_income_group(country) -> str`}</code></pre>

      <h2>Example</h2>
      <pre><code>{`from hermes.countries import get_country_metadata, list_countries

meta = get_country_metadata("USA")
print(meta["name"])        # "United States"
print(meta["region"])      # "North America"
print(meta["neighbors"])   # ["CAN", "MEX"]

for c in list_countries()[:5]:
    print(c["iso_code"], c["name"])`}</code></pre>

      <h2>Data Shape</h2>
      <p>Each entry in <code>COUNTRY_META</code> has:</p>
      <table>
        <thead><tr><th>Field</th><th>Type</th><th>Example</th></tr></thead>
        <tbody>
          <tr><td>name</td><td>str</td><td>"United States"</td></tr>
          <tr><td>region</td><td>str</td><td>"North America"</td></tr>
          <tr><td>income_group</td><td>str</td><td>"High income"</td></tr>
          <tr><td>capital</td><td>str</td><td>"Washington, D.C."</td></tr>
          <tr><td>currency</td><td>str</td><td>"USD"</td></tr>
          <tr><td>neighbors</td><td>list[str]</td><td>["CAN", "MEX"]</td></tr>
        </tbody>
      </table>
    </>
  );
}
