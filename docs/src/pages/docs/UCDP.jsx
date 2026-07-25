export default function UCDPDoc() {
  return (
    <>
      <h1>UCDP Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/ucdp.py</code></p>
      <p><strong>Class:</strong> <code>UCDP(BaseConnector)</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches conflict event data from the Uppsala Conflict Data Program.
        Provides battle-related deaths, organized violence events, and conflict
        type classifications.
      </p>

      <h2>Key Methods</h2>
      <pre><code>{`fetch(country="", indicator="battle_deaths") -> pd.DataFrame`}</code></pre>
      <p>Supports indicators: <code>battle_deaths</code>, <code>ged</code>, <code>conflict_type</code></p>

      <h2>Available Countries</h2>
      <p>AFG, IRQ, SYR, UKR, YEM, SOM, SSD, MMR, ETH, COD, SDN, COL, MEX</p>

      <h2>Date Range</h2>
      <p>1989-01-01 to present</p>
    </>
  );
}
