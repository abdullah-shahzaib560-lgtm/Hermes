export default function FeaturesDoc() {
  return (
    <>
      <h1>Features API</h1>
      <p><strong>Files:</strong> <code>hermes/features/country_risk_features/</code></p>

      <h2>What It Does</h2>
      <p>
        The pipeline computes <strong>58 country risk features</strong> across five dimensions
        and exposes them in two ways: a snapshot dict for one country, and a multi-country
        time-series panel for ML. Every feature is a decorated function registered in a lineage
        graph.
      </p>

      <h2>Feature Groups</h2>
      <table>
        <thead>
          <tr>
            <th>Group</th>
            <th>Count</th>
            <th>Examples</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>economic</code></td>
            <td>18</td>
            <td>gdp_growth_yoy, inflation_cpi_yoy, unemployment_rate, government_debt_gdp, banking_sector_health, ...</td>
          </tr>
          <tr>
            <td><code>geopolitical</code></td>
            <td>21</td>
            <td>conflict_event_count_30d, goldstein_scale_avg_30d, battle_deaths_90d, sanctions_count_active, corruption_perception_index, regime_type, ...</td>
          </tr>
          <tr>
            <td><code>security</code></td>
            <td>7</td>
            <td>military_spending_gdp, alliance_strength_score, arms_imports_12m, nato_member, ...</td>
          </tr>
          <tr>
            <td><code>social</code></td>
            <td>6</td>
            <td>human_development_index, fragile_state_index, gini_coefficient, poverty_headcount_ratio, ...</td>
          </tr>
          <tr>
            <td><code>environmental</code></td>
            <td>6</td>
            <td>climate_vulnerability_score, food_price_index_change_yoy, water_stress_index, ...</td>
          </tr>
        </tbody>
      </table>

      <h2>Snapshot: Country Risk Dict</h2>
      <pre><code>{`risk = hr.features.get_country_risk_features("UKR")

risk["economic"]["gdp_growth_yoy"]
risk["geopolitical"]["sanctions_count_active"]
risk["metadata"]["last_updated"]`}</code></pre>
      <p>
        Returns a nested dict with one key per group, plus <code>metadata</code>. Features that
        fail (no data, connector error) come back as <code>NaN</code> rather than crashing.
      </p>

      <h2>Feature Modes</h2>
      <p>Every feature function accepts a <code>mode</code> argument:</p>
      <table>
        <thead>
          <tr>
            <th>Mode</th>
            <th>Returns</th>
            <th>Use case</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>"F"</code></td>
            <td><code>float</code> / <code>int</code> / <code>bool</code></td>
            <td>Latest value for dashboards and snapshots</td>
          </tr>
          <tr>
            <td><code>"ML"</code></td>
            <td><code>pd.Series</code> (monthly index)</td>
            <td>Time series for training and forecasting</td>
          </tr>
        </tbody>
      </table>
      <pre><code>{`# Call a single feature directly
hr.lf.eco.gdp_growth_yoy(country_code="USA", mode="F")
# -> 2.1

# Or as a monthly series
hr.lf.eco.inflation_cpi_yoy(country_code="DEU", mode="ML")
# -> 2023-01-01    4.3
#    2023-02-01    4.1
#    ...`}</code></pre>

      <h2>Training Panels</h2>
      <p>
        Build a multi-country, monthly panel for ML by passing the feature functions and
        country codes:
      </p>
      <pre><code>{`panel = hr.features.build_training_panel(
    fns=[
        hr.lf.eco.gdp_growth_yoy,
        hr.lf.eco.inflation_cpi_yoy,
        hr.lf.geo.conflict_event_count_30d,
    ],
    countries=["USA", "UKR", "DEU"],
)
# DataFrame with (country_iso3, date) MultiIndex
# Columns: gdp_growth_yoy, inflation_cpi_yoy, conflict_event_count_30d`}</code></pre>

      <h2>Listing Features</h2>
      <pre><code>{`# All feature callables
hr.list_features

# Registry with grouped access
hr.lf.eco      # economic features
hr.lf.geo      # geopolitical features
hr.lf.sec      # security features
hr.lf.soc      # social features
hr.lf.env      # environmental features`}</code></pre>

      <h2>Lineage &amp; Decorator</h2>
      <p><strong>File:</strong> <code>hermes/core/feature_decorator.py</code></p>
      <p>
        Each feature is registered via the <code>@feature</code> decorator with its name,
        group, dependencies, and a compute description. A global <code>LineageGraph</code>
        collects these registrations and can resolve a group into dependency-ordered execution
        tiers:
      </p>
      <pre><code>{`from hermes.core.feature_decorator import lineagegraph

plan = lineagegraph.resolve_group("economic_features")
plan.tiers        # execution order (dependency-ordered)
plan.all_features # every feature name in the group

lineagegraph.save("lineage.json")  # persist the graph
lineagegraph.load("lineage.json")  # restore it`}</code></pre>
    </>
  );
}
