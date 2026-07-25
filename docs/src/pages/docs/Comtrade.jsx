export default function ComtradeDoc() {
  return (
    <>
      <h1>Comtrade Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/comtrade.py</code></p>
      <p><strong>Class:</strong> <code>Comtrade(BaseConnector)</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches international trade flow data from the UN Comtrade database.
        Provides exports, imports, and trade balance by commodity codes and
        partner countries for trade dependency and supply chain analysis.
      </p>

      <h2>Key Methods</h2>
      <pre><code>{`fetch(country="", indicator="exports") -> pd.DataFrame`}</code></pre>
      <p>Supports indicators: <code>exports</code>, <code>imports</code>, <code>re_exports</code>, <code>trade_balance</code></p>

      <h2>Available Countries</h2>
      <p>USA, CHN, DEU, JPN, GBR, FRA, KOR, NLD, ITA, CAN, MEX, IND, BRA, RUS</p>

      <h2>Date Range</h2>
      <p>1962-01-01 to present</p>
    </>
  );
}
