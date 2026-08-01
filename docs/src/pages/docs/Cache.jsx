export default function CacheDoc() {
  return (
    <>
      <h1>Data Cache</h1>
      <p><strong>File:</strong> <code>hermes/core/cache.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>RawCache</code> stores every raw API response as a Parquet file on disk, keyed
        by a SHA-256 hash of the source and request parameters. Connectors read from the cache
        instead of re-hitting the API, which keeps repeated calls fast and avoids burning
        rate limits.
      </p>

      <h2>Storage</h2>
      <ul>
        <li>Default location: <code>~/.hermes_cache/raw/</code></li>
        <li>Layout: <code>{`~/.hermes_cache/raw/{source}/{hash}.parquet`}</code></li>
        <li>Each file is paired with a <code>{`{hash}.meta.json`}</code> sidecar (source, params, cached_at, rows, columns)</li>
        <li>Default TTL: <code>24 hours</code></li>
      </ul>

      <h2>Per-Source TTLs</h2>
      <p>Each connector sets its own TTL based on how often the underlying data changes:</p>
      <table>
        <thead>
          <tr>
            <th>Source</th>
            <th>TTL</th>
            <th>Why</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>GDELT</td>
            <td>6 hours</td>
            <td>Event data updates constantly.</td>
          </tr>
          <tr>
            <td>World Bank</td>
            <td>7 days</td>
            <td>Indicators released weekly.</td>
          </tr>
          <tr>
            <td>IMF</td>
            <td>7 days</td>
            <td>Dataflows refresh weekly.</td>
          </tr>
          <tr>
            <td>OpenSanctions</td>
            <td>30 days</td>
            <td>Sanctions lists change slowly.</td>
          </tr>
        </tbody>
      </table>

      <h2>API</h2>

      <h3><code>get(source, params, ttl=None) → DataFrame</code></h3>
      <p>
        Reads a cached response. Raises <code>CacheMiss</code> if the file is missing, expired
        (file is deleted), or corrupted (file is deleted and re-fetched).
      </p>

      <h3><code>put(source, params, df)</code></h3>
      <p>Writes a DataFrame to the cache with its metadata sidecar.</p>

      <h3><code>get_or_fetch(source, params, fetch_fn, force=False, ttl=None) → DataFrame</code></h3>
      <p>
        The workhorse used by every connector: try the cache first, and only call
        <code>fetch_fn</code> on a miss. Pass <code>force=True</code> to bypass the cache and
        refresh from the API.
      </p>
      <pre><code>{`df = cache.get_or_fetch(
    source="world_bank",
    params={"country": "USA", "indicator": "NY.GDP.MKTP.KD.ZG"},
    fetch_fn=lambda: api_call(),
    force=False,
    ttl=timedelta(days=7),
)`}</code></pre>

      <h3><code>clear(older_than: timedelta | None = None)</code></h3>
      <p>Deletes cached files (and their metadata). Without arguments it wipes everything; with a <code>timedelta</code> it only removes entries older than that age.</p>

      <h3><code>stats() → dict</code></h3>
      <p>Returns <code>total_files</code>, <code>by_source</code>, <code>hits</code>, <code>misses</code>, and <code>hit_rate</code> per source.</p>
    </>
  );
}
