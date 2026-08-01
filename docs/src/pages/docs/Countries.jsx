export default function CountriesDoc() {
  return (
    <>
      <h1>Country Data</h1>
      <p><strong>File:</strong> <code>hermes/core/countries.py</code></p>

      <h2>What It Does</h2>
      <p>
        Defines the <code>countries</code> list — every ISO 3166-1 alpha-3 country code the SDK
        supports. Connectors and feature functions expect these three-letter codes (e.g.
        <code>"USA"</code>, <code>"UKR"</code>, <code>"DEU"</code>).
      </p>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(opensanction_api=...)

# Full list of supported codes
print(hr.list_countries)
# ['AFG', 'ALA', 'ALB', 'DZA', 'ASM', ...]

# Iterate countries to build panels or batch snapshots
for code in hr.list_countries:
    print(code)`}</code></pre>

      <h2>Validation</h2>
      <p>
        Feature functions validate country codes with <code>pycountry</code> and raise a
        <code>RuntimeError</code> for invalid ISO3 codes:
      </p>
      <pre><code>{`# Raises: RuntimeError("The XYZ is not iso3")
hr.features.get_country_risk_features("XYZ")`}</code></pre>

      <h2>Notes</h2>
      <ul>
        <li>The list covers roughly 240 codes, including territories and dependencies.</li>
        <li>Coverage varies per connector — some indicators are not available for every territory.</li>
        <li>Connectors handle the ISO3 → ISO2 / FIPS conversions internally where needed.</li>
      </ul>
    </>
  );
}
