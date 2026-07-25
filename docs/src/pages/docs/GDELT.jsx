export default function GDELTDoc() {
  return (
    <>
      <h1>GDELT Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/gdelt.py</code></p>
      <p><strong>Class:</strong> <code>GDELT(BaseConnector)</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches real-time conflict event data from the Global Database of Events,
        Language, and Tone (GDELT). Provides Goldstein scale scores and news tone
        metrics for geopolitical risk assessment.
      </p>

      <h2>Key Methods</h2>
      <pre><code>{`fetch(country="", indicator="events") -> pd.DataFrame`}</code></pre>
      <p>Supports indicators: <code>events</code>, <code>gkg</code> (Global Knowledge Graph), <code>summaries</code></p>

      <h2>Available Countries</h2>
      <p>USA, GBR, DEU, FRA, CHN, RUS, IRN, PRK, ISR, SAU, UKR, AFG, IRQ, SYR</p>

      <h2>Date Range</h2>
      <p>1979-01-01 to present</p>
    </>
  );
}
