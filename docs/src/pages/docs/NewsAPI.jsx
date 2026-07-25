export default function NewsAPIDoc() {
  return (
    <>
      <h1>NewsAPI Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/newsapi.py</code></p>
      <p><strong>Class:</strong> <code>NewsAPI(BaseConnector)</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches news article metadata, sentiment scores, and coverage intensity
        for real-time event detection and sentiment analysis.
      </p>

      <h2>Key Methods</h2>
      <pre><code>{`fetch(country="", indicator="headlines") -> pd.DataFrame`}</code></pre>
      <p>Supports indicators: <code>headlines</code>, <code>everything</code>, <code>sentiment</code>, <code>source_coverage</code></p>

      <h2>Available Countries</h2>
      <p>USA, GBR, DEU, FRA, JPN, CHN, IND, BRA, CAN, AUS, RUS, ZAF</p>
    </>
  );
}
