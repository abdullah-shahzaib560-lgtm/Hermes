export default function GettingStarted() {
  return (
    <>
      <h1>Getting Started</h1>

      <h2>Installation</h2>
      <pre><code>{`# Clone the repository
git clone https://github.com/ryomenhaider/Hermes.git
cd Hermes

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .`}</code></pre>

      <h2>Quick Start</h2>
      <pre><code>{`from hermes import Hermes

# Initialize the SDK
hr = Hermes(api_keys={"fred": "YOUR_FRED_API_KEY"})

# Fetch economic data from FRED
df = hr.fred.fetch(country="USA", indicator="GDPC1")
print(df.head())

# Get comprehensive risk features for a country
risk = hr.get_country_risk_features("USA", "2024-12-31")
print(risk["gdp_growth_yoy"])`}</code></pre>

      <h2>Environment Setup</h2>
      <p>Create a <code>.env</code> file in the project root:</p>
      <pre><code>{`FRED_API=your_fred_api_key_here`}</code></pre>
      <p>FRED requires a free API key (any email). BIS, IMF, and World Bank require no authentication.</p>

      <h2>Architecture Overview</h2>
      <p>Hermes is organized into three layers:</p>
      <table>
        <thead>
          <tr><th>Layer</th><th>Path</th><th>Purpose</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Connectors</strong></td><td><code>hermes/sources/</code></td><td>Fetch data from free APIs, normalize to standard DataFrames</td></tr>
          <tr><td><strong>Features</strong></td><td><code>hermes/features/</code></td><td>Engineer derived risk indicators from raw connector data</td></tr>
          <tr><td><strong>Cache</strong></td><td><code>hermes/_cache.py</code></td><td>Parquet file cache with TTL expiration</td></tr>
        </tbody>
      </table>

      <h2>Quick Example — Full Pipeline</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes(api_keys={"fred": os.getenv("FRED_API")})

# Get risk features for a country
risk = hr.get_country_risk_features("USA", "2024-12-31")

# Access individual indicators
print(risk["gdp_growth_yoy"])
print(risk["inflation_cpi_yoy"])
print(risk["unemployment_rate"])
print(risk["regime_classification"])

# List all available connectors
for c in hr.list_connectors():
    print(c["name"], c["type"])`}</code></pre>
    </>
  );
}
