import type { Metadata } from "next";
import {
  DocTitle,
  Lead,
  H2,
  P,
  Callout,
  PrevNext,
  Table,
} from "@/components/Doc";
import { CodeBlock } from "@/components/CodeBlock";

export const metadata: Metadata = {
  title: "Connectors",
  description: "Every Hermes data source connector and how to use it.",
};

const CONTRACT = `class WorldBankConnector:
    async def fetch(self) -> list[dict]:
        ...
        return records`;

export default function ConnectorsPage() {
  return (
    <article>
      <DocTitle kicker="Core Concepts">Connectors</DocTitle>
      <Lead>
        Every source in Hermes speaks the same language: an async <code>fetch()</code> that
        returns canonical records. Ten connectors ship out of the box.
      </Lead>

      <H2 id="contract">The connector contract</H2>
      <P>
        Each connector package exposes a <code>fetch()</code> method alongside a parser, a
        normalizer and a set of field mappings. That means you can swap sources without changing
        your pipeline code.
      </P>
      <CodeBlock code={CONTRACT} title="python" />
      <P>
        Connectors also sit behind the <code>RawCache</code>, so identical fetches are served
        from parquet instead of hitting the network again.
      </P>

      <H2 id="global-macro">Global macro</H2>
      <Table
        head={["Connector", "Source", "Notes"]}
        rows={[
          ["WorldBank", "data.worldbank.org", "Country-level indicators via the v2 API. Supports indicator + years."],
          ["IMF", "IMF SDMX", "Global financial & macro data through the sdmx library."],
          ["FRED", "fred.stlouisfed.org", "US & global economic time series. Needs FRED_API key."],
          ["GDELT", "GDELT project", "Global news / event data. Connector is currently a stub."],
        ]}
      />

      <H2 id="markets">Markets</H2>
      <Table
        head={["Connector", "Source", "Notes"]}
        rows={[
          ["Yfinance", "Yahoo Finance", "Prices, fundamentals and crypto history via yfinance."],
          ["FINNHUB", "Finnhub", "Real-time & historical market data. Needs FINNHUB_API key."],
          ["Binance", "Binance", "Crypto market data. Symbols are preconfigured in constants."],
        ]}
      />

      <H2 id="identity-risk">Identity & risk</H2>
      <Table
        head={["Connector", "Source", "Notes"]}
        rows={[
          ["SECEDGAR", "SEC EDGAR", "Company filings. Uses sec-cik-mapper for ticker → CIK."],
          ["OpenSanction", "OpenSanctions", "Sanctions lists. Needs OPEN_SANCTIONS_API key."],
          ["PUBLIC_DATASET", "Bundled", "Local CSV datasets (CRS, HDI, SIPRI, NATO, FSI…)."],
        ]}
      />

      <H2 id="usage">Example</H2>
      <P>Pull an indicator from the World Bank through the facade:</P>
      <CodeBlock
        title="python"
        code={`from hermes import Hermes

hermes = Hermes()

data = hermes.world_bank.fetch(
    indicator="SP.POP.TOTL",
    years=[2021, 2022],
)`}
      />

      <Callout title="Async" tone="accent">
        Connectors are async. If you call them outside the facade&apos;s event loop, wrap calls in
        <code> asyncio.run(...)</code> or run them inside an async context.
      </Callout>

      <PrevNext
        prev={{ title: "Quickstart", href: "/docs/quickstart" }}
        next={{ title: "Features", href: "/docs/features" }}
      />
    </article>
  );
}
