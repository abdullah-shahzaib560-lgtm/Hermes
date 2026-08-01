export default function GettingStarted() {
  return (
    <>
      <h1>Getting Started</h1>

      <h2>Requirements</h2>
      <ul>
        <li>Python <strong>&gt;= 3.11</strong></li>
        <li><a href="https://docs.astral.sh/uv/" target="_blank">uv</a> for dependency management</li>
        <li>An <a href="https://www.opensanctions.org/" target="_blank">OpenSanctions</a> API key</li>
      </ul>

      <h2>Installation</h2>
      <pre><code>{`git clone <repo-url> Hermes
cd Hermes
uv sync --extra dev`}</code></pre>
      <p>The <code>dev</code> extra pulls in pytest, ruff, mypy, and other development tools. Use plain <code>uv sync</code> for a production install.</p>

      <h2>Configuration</h2>
      <p>Copy the environment template and add your OpenSanctions API key:</p>
      <pre><code>{`cp .env.example .env
# OPEN_SANCTIONS_API=your_key_here`}</code></pre>
      <blockquote>
        The API key is required. Instantiating <code>Hermes</code> without one raises a <code>KeyError</code>.
      </blockquote>

      <h2>Quick Start</h2>
      <pre><code>{`from hermes import Hermes
from dotenv import load_dotenv
import os

load_dotenv()

hr = Hermes(opensanction_api=os.getenv("OPEN_SANCTIONS_API"))

# Every supported country code (ISO3)
print(hr.list_countries)

# All available feature functions
print(hr.list_features)`}</code></pre>

      <h2>What's Next</h2>
      <ul>
        <li><a href="/docs/hermes">Hermes Class</a> — the SDK facade and its methods</li>
        <li><a href="/docs/features">Features API</a> — country risk snapshots and ML panels</li>
        <li><a href="/docs/cache">Data Cache</a> — how raw responses are stored</li>
      </ul>
    </>
  );
}
