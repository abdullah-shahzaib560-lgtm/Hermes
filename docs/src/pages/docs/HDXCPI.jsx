export default function HDXCPIDoc() {
  return (
    <>
      <h1><code>HDXCPI</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/hdx_cpi.py</code></p>

      <h2>What It Does</h2>
      <p>
        Reads the Corruption Perceptions Index (CPI) from a bundled CSV dataset
        (<code>res/global_cpi_all.csv</code>), powered by the
        <a href="https://data.humdata.org/" target="_blank">Humanitarian Data Exchange</a>.
        No network calls — data ships with the package.
      </p>

      <h2>Usage</h2>
      <pre><code>{`from hermes.sources.hdx_cpi import HDXCPI

cpi = HDXCPI()

df = cpi.fetch(country="USA")`}</code></pre>

      <h3><code>fetch(country) → DataFrame</code></h3>
      <p>Filters the CPI dataset to a single ISO3 country code.</p>

      <h2>Output Columns</h2>
      <table>
        <thead>
          <tr>
            <th>Column</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>iso3</code></td>
            <td>ISO3 country code</td>
          </tr>
          <tr>
            <td><code>year</code></td>
            <td>Observation year</td>
          </tr>
          <tr>
            <td><code>score</code></td>
            <td>CPI score (0-100)</td>
          </tr>
        </tbody>
      </table>

      <h2>In the Pipeline</h2>
      <p>
        This connector backs the <code>corruption_perception_index</code> feature in the
        geopolitical group.
      </p>
    </>
  );
}
