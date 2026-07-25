export default function CacheDoc() {
  return (
    <>
      <h1><code>DataCache</code></h1>
      <p><strong>File:</strong> <code>hermes/_cache.py</code></p>

      <h2>What It Does</h2>
      <p>
        <code>DataCache</code> is a simple file-based cache backed by Parquet files.
        It reduces redundant API calls by storing fetched DataFrames on disk with
        configurable TTL expiration.
      </p>

      <h2>Constructor</h2>
      <pre><code>{`DataCache(cache_dir: str | Path | None = None)`}</code></pre>
      <p>Defaults to <code>~/.hermes_cache</code> if no directory is provided.</p>

      <h2>Key Methods</h2>
      <pre><code>{`# Retrieve cached data
get(*args, **kwargs) -> pd.DataFrame | None

# Store data with TTL (seconds)
set(df, ttl=3600, *args, **kwargs) -> None`}</code></pre>

      <h2>How It Works</h2>
      <ul>
        <li>Cache keys are SHA-256 hashes of the positional and keyword arguments</li>
        <li>Data is stored as Parquet files in a sharded directory structure (<code>xx/yy/key.parquet</code>)</li>
        <li>TTL metadata is stored alongside in a JSON sidecar file</li>
        <li>Expired entries are automatically evicted on read</li>
      </ul>

      <h2>Usage</h2>
      <pre><code>{`from hermes._cache import DataCache

cache = DataCache("my_cache_dir")

cached = cache.get("fred", "GDPC1")
if cached is not None:
    df = cached
else:
    df = fetch_from_api()
    cache.set(df, ttl=7200, "fred", "GDPC1")`}</code></pre>
    </>
  );
}
