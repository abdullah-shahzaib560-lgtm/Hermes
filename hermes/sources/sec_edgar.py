import asyncio
import logging
from typing import Literal, Dict

from datetime import timedelta
from functools import partial

import aiohttp
import pandas as pd

from hermes.core.helper import get_CIK

logger = logging.getLogger(__name__)


class SECEDGAR:

    BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts"

    CONCEPTS = {
        # Income Statement

        "revenue": [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "Revenues",
        ],
        "cost_of_revenue": [
            "CostOfRevenue",
            "CostOfGoodsAndServicesSold",
        ],
        "gross_profit": [
            "GrossProfit",
        ],
        "operating_income": [
            "OperatingIncomeLoss",
        ],
        "operating_expenses": [
            "OperatingExpenses",
        ],
        "net_income": [
            "NetIncomeLoss",
        ],
        "interest_expense": [
            "InterestExpenseNonOperating",
            "InterestExpenseNonOperatingCurrent",
        ],
        "income_tax_expense": [
            "IncomeTaxExpenseBenefit",
        ],
        "eps_basic": [
            "EarningsPerShareBasic",
        ],
        "eps_diluted": [
            "EarningsPerShareDiluted",
        ],

        # Balance Sheet

        "cash": [
            "CashAndCashEquivalentsAtCarryingValue",
        ],
        "short_term_investments": [
            "ShortTermInvestments",
            "MarketableSecuritiesCurrent",
            "AvailableForSaleSecuritiesDebtSecuritiesCurrent",
        ],
        "current_assets": [
            "AssetsCurrent",
        ],
        "total_assets": [
            "Assets",
        ],
        "current_liabilities": [
            "LiabilitiesCurrent",
        ],
        "total_liabilities": [
            "Liabilities",
        ],
        "equity": [
            "StockholdersEquity",
            "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        ],

        "current_debt": [
            "LongTermDebtCurrent",
            "ShortTermBorrowings",
            "ShortTermDebt",
        ],
        "noncurrent_debt": [
            "LongTermDebtNoncurrent",
            "LongTermDebt",
        ],

        "operating_cash_flow": [
            "NetCashProvidedByUsedInOperatingActivities",
        ],
        "investing_cash_flow": [
            "NetCashProvidedByUsedInInvestingActivities",
        ],
        "financing_cash_flow": [
            "NetCashProvidedByUsedInFinancingActivities",
        ],
        "capex": [
            "PaymentsToAcquirePropertyPlantAndEquipment",
        ],

        # Shares

        "shares_outstanding": [
            "EntityCommonStockSharesOutstanding",
        ],
        "weighted_avg_basic_shares": [
            "WeightedAverageNumberOfSharesOutstandingBasic",
        ],
        "weighted_avg_diluted_shares": [
            "WeightedAverageNumberOfDilutedSharesOutstanding",
        ],
    }

    def __init__(
        self,
        email: str,
        timeout: float = 30.0,
        retries: int = 3,
    ):
        self._email = email
        self._timeout = timeout
        self._retries = retries


    def _resolve_cik(self, company: str) -> str:

        company = str(company).strip()

        # Already a CIK
        if company.upper().startswith("CIK"):
            cik = company.upper().replace("CIK", "")
        elif company.isdigit():
            cik = company
        else:
            cik = get_CIK(ticker=company)

        cik = str(cik).replace("CIK", "").zfill(10)

        return cik

    async def _request(self, url: str) -> dict:

        headers = {
            "User-Agent": f"Sentinel {self._email}"
        }

        timeout = aiohttp.ClientTimeout(
            total=self._timeout
        )

        async with aiohttp.ClientSession(
            timeout=timeout,
            trust_env=True,
        ) as client:

            for attempt in range(self._retries):

                try:

                    async with client.get(
                        url=url,
                        headers=headers,
                    ) as response:

                        if response.status == 404:
                            logger.warning(
                                "SEC returned 404: %s",
                                url,
                            )
                            return {}

                        response.raise_for_status()

                        return await response.json()

                except asyncio.TimeoutError:

                    if attempt == self._retries - 1:
                        raise

                    logger.warning(
                        "SEC request timeout. Retry %s/%s",
                        attempt + 1,
                        self._retries,
                    )

                except aiohttp.ClientResponseError as e:

                    if e.status == 404:
                        logger.warning(
                            "SEC returned 404: %s",
                            url,
                        )
                        return {}

                    if attempt == self._retries - 1:
                        raise

                    logger.warning(
                        "SEC HTTP error %s. Retry %s/%s",
                        e.status,
                        attempt + 1,
                        self._retries,
                    )

                await asyncio.sleep(2 ** attempt)

        return {}


    async def _fetch_full(
        self,
        company: str,
    ) -> dict:

        cik = self._resolve_cik(company)

        url = f"{self.BASE_URL}/CIK{cik}.json"

        return await self._request(url)

    @staticmethod
    def _find_concept(
        facts: dict,
        candidates: list[str],
    ):
        for concept in candidates:

            if concept in facts:

                return concept, facts[concept]

        return None, None

 
    @staticmethod
    def _extract_units(
        concept_data: dict,
    ) -> list[tuple[str, list[dict]]]:
        units = concept_data.get("units", {})

        return list(units.items())

 
    def _extract_metric(
        self,
        facts: dict,
        metric: str,
        candidates: list[str],
    ) -> pd.DataFrame:

        concept_name, concept_data = self._find_concept(
            facts,
            candidates,
        )

        if concept_data is None:

            logger.warning(
                "No SEC concept found for metric '%s'. "
                "Tried: %s",
                metric,
                candidates,
            )

            return pd.DataFrame()

        rows = []

        for unit, observations in self._extract_units(
            concept_data
        ):

            for observation in observations:

                rows.append(
                    {
                        "metric": metric,
                        "concept": concept_name,
                        "unit": unit,

                        "start": observation.get("start"),
                        "end": observation.get("end"),

                        "value": observation.get("val"),

                        "accession": observation.get("accn"),

                        "fiscal_year": observation.get("fy"),
                        "fiscal_period": observation.get("fp"),

                        "form": observation.get("form"),
                        "filed": observation.get("filed"),

                        "frame": observation.get("frame"),
                    }
                )

        return pd.DataFrame(rows)

    # BUILD IMPORTANT DATASET
 
    def _extract_important(
        self,
        data: dict,
        company: str,
    ) -> pd.DataFrame:

        if not data:
            return pd.DataFrame()

        facts = data.get("facts", {}).get(
            "us-gaap",
            {},
        )

        if not facts:
            logger.warning(
                "No us-gaap facts found for %s",
                company,
            )
            return pd.DataFrame()

        cik = self._resolve_cik(company)

        all_frames = []

        for metric, candidates in self.CONCEPTS.items():

            df = self._extract_metric(
                facts=facts,
                metric=metric,
                candidates=candidates,
            )

            if not df.empty:

                df.insert(
                    0,
                    "cik",
                    cik,
                )

                all_frames.append(df)

        if not all_frames:
            return pd.DataFrame()

        result = pd.concat(
            all_frames,
            ignore_index=True,
        )

        # Dates
        result["start"] = pd.to_datetime(
            result["start"],
            errors="coerce",
        )

        result["end"] = pd.to_datetime(
            result["end"],
            errors="coerce",
        )

        result["filed"] = pd.to_datetime(
            result["filed"],
            errors="coerce",
        )

        # Sort
        result = result.sort_values(
            [
                "metric",
                "end",
                "filed",
            ]
        ).reset_index(drop=True)

        return result

    async def fetch(
        self,
        company: str,
        mode: Literal["full", "imp"] = "imp",
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pd.DataFrame | Dict:

        cache_params = {
            "company": company,
            "mode": mode,
        }

        return await self._cache.get_or_fetch(
            source="sec_edgar",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                company=company,
                mode=mode,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
    
if __name__ == "__main__":

    async def main():

        sec = SECEDGAR(
            email=""
        )

        df = await sec.fetch(
            company="CIK0000320193",
            mode="imp",
        )

        print(df)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nMetrics found:")
        print(df["metric"].unique())

    asyncio.run(main())