export default function HermesDoc() {
  return (
    <>
      <h1><code>Hermes</code> Class</h1>
      <p><strong>File:</strong> <code>hermes/__init__.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>Hermes</code> class is the main entry point of the SDK. It composes every
        connector and the feature pipeline into a single object, so all functionality is
        reachable through one import:
      </p>
      <pre><code>{`from hermes import Hermes`}</code></pre>

      <h2>Constructor</h2>
      <pre><code>{`Hermes(
    opensanction_api: str,
    cache_dir: str | None = None,
    use_cache: bool = True,
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
            <td><code>opensanction_api</code></td>
            <td>—</td>
            <td>OpenSanctions API key. Required; raises <code>KeyError</code> if empty.</td>
          </tr>
          <tr>
            <td><code>cache_dir</code></td>
            <td><code>~/.hermes_cache/raw</code></td>
            <td>Directory for the raw Parquet cache.</td>
          </tr>
          <tr>
            <td><code>use_cache</code></td>
            <td><code>True</code></td>
            <td>Set to <code>False</code> to disable caching entirely.</td>
          </tr>
        </tbody>
      </table>

      <h2>Attributes</h2>
      <table>
        <thead>
          <tr>
            <th>Attribute</th>
            <th>Type</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>hr.features</code></td>
            <td><code>pipeline</code></td>
            <td>Country risk pipeline — snapshots and training panels.</td>
          </tr>
          <tr>
            <td><code>hr.lf</code></td>
            <td><code>features</code></td>
            <td>Feature registry — access every feature function.</td>
          </tr>
          <tr>
            <td><code>hr.list_features</code></td>
            <td><code>list</code></td>
            <td>All ~60 feature functions, ready to call.</td>
          </tr>
          <tr>
            <td><code>hr.list_countries</code></td>
            <td><code>list[str]</code></td>
            <td>All supported ISO3 country codes.</td>
          </tr>
          <tr>
            <td><code>hr.world_bank</code></td>
            <td><code>World_bank</code></td>
            <td>World Bank connector.</td>
          </tr>
          <tr>
            <td><code>hr.imf</code></td>
            <td><code>IMF</code></td>
            <td>IMF SDMX connector.</td>
          </tr>
          <tr>
            <td><code>hr.gdelt</code></td>
            <td><code>GDELT</code></td>
            <td>GDELT events connector.</td>
          </tr>
          <tr>
            <td><code>hr.opensanction</code></td>
            <td><code>OpenSanction</code></td>
            <td>OpenSanctions connector.</td>
          </tr>
        </tbody>
      </table>

      <h2>Methods</h2>

      <h3><code>clear_cache(older_than: str | None = None)</code></h3>
      <p>Deletes cached Parquet files. Pass a duration string like <code>"24h"</code>, <code>"7d"</code>, or <code>"2w"</code> to only remove entries older than that.</p>
      <pre><code>{`hr.clear_cache()                 # wipe everything
hr.clear_cache(older_than="7d") # only entries older than 7 days`}</code></pre>

      <h3><code>cache_stats() → dict</code></h3>
      <p>Returns cache usage: total files, files per source, hits, misses, and hit rate per source.</p>
      <pre><code>{`stats = hr.cache_stats()
# {"total_files": 42, "by_source": {...}, "hits": {...}, "misses": {...}, "hit_rate": {...}}`}</code></pre>
      <p>When caching is disabled, returns an empty stats dict.</p>
    </>
  );
}
