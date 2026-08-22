import asyncio

from hermes.core.models.analysis.fundamental import CompanyFundamental
from hermes.sources.finnhub import FINNHUB
from hermes.sources.lib.sec_tag import SEC_TAG_MAP
from hermes.sources.sec_edgar import SECEDGAR
from hermes.sources.fred import FRED
from hermes.sources.yf import Yfinance

class fundamenatals:

    def __init__(
            self, 
            finnhub_api: str, 
            sec_email: str, 
            sec_username: str,
            fred_api: str,
        ):
        self.finn: FINNHUB = FINNHUB(api=finnhub_api)
        self.sec: SECEDGAR = SECEDGAR(username=sec_username, email=sec_email)
        self.fred: FRED = FRED(api=fred_api)
        self._yf = Yfinance()

    def extract_funds_sec(data: dict) -> dict:
        facts = data["facts"]["us-gaap"]
        result = {}

        for field, tags in SEC_TAG_MAP.items():
            result[field] = None

            for tag in tags:
                if tag in facts:
                    result[field] = facts[tag]
                    break

        return result

    async def _yf_data(self, symbol: str):
        return {
            "earnings_surprise ": next(iter((self._yf.fetch(endpoint='earnings_history', symbol=symbol)['surprisePercent']).values())),
            "eps_estimate": self._yf.fetch(endpoint='eps_estimate', symbol=symbol)['avg']['0q'],
            "revenue_estimate": self._yf.fetch(symbol=symbol, endpoint='revenue_estimate')['avg']['0y']
        } 

    async def finn_profile(self, symbol: str):
        data = await self.finn.fetch(endpoint='profile', symbol=symbol)
        return data

    async def company_peers(self, symbol: str):
        data = await self.finn.fetch(endpoint='peers', symbol=symbol)
        return data

    async def finn_metrics(self, symbol: str):
        data = await self.finn.fetch(endpoint='metric', symbol=symbol)
        return data

    async def finn_qoute(self, symbol: str):
        return await self.finn.fetch(endpoint='quote', symbol=symbol)['c']

    async def macro(self):
        macro_gdp = await self.fred.fetch(series_id="GDPC1")
        macro_gdp_growth= await self.fred.fetch(series_id="A191RL1Q225SBEA"),
        macro_inflation= await self.fred.fetch(series_id="CPIAUCSL"),
        macro_interest_rates= await self.fred.fetch(series_id="FEDFUNDS"),
        macro_unemployment= await self.fred.fetch(series_id="UNRATE"),
        macro_government_debt= await self.fred.fetch(series_id="GFDEBTN"),
        macro_exchange_rates =  await self.fred.fetch(series_id="RTWEXBGS"),

        return {
            "macro_gdp" : macro_gdp,
            "macro_gdp_growth":macro_gdp_growth,
            "macro_inflation":macro_inflation,
            "macro_interest_rates":macro_interest_rates,
            "macro_unemployment":macro_unemployment,
            "macro_government_debt":macro_government_debt,
            "macro_exchange_rates":macro_exchange_rates,
        }

async def get_fundamentels(symbol: str):
    fund = fundamenatals(api='da45rr9r01qo2j8743egda45rr9r01qo2j8743f0',email='haiderali.dev95@gmail.com',username='Sentinel')
    raw_sec = await fund.sec.fetch(company=symbol)
    sec_funds = fund.extract_funds_sec(data=raw_sec)
    metric = await fund.finn_metrics(symbol=symbol)
    macro = await fund.macro()
    yf_data = await fund._yf_data(symbol=symbol)

    return CompanyFundamental(

        symbol= symbol,
        filing_date= 0,
        fiscal_period=  0,
        fiscal_year= 0,
        filing_type= 0,

        pre_tax_income= sec_funds['pre_tax_income'],
        revenue= sec_funds['revenue'],
        cost_of_revenue= sec_funds['cost_of_revenue'],
        gross_profit= sec_funds['gross_profit'],
        operating_expenses= sec_funds['operating_expenses'],
        operating_income= sec_funds['operating_income'],
        interest_expense= sec_funds['interest_expense'],
        income_tax_expense= sec_funds['income_tax_expense'],
        net_income= sec_funds['net_income'],
        eps_basic= sec_funds['eps_basic'],
        eps_diluted= sec_funds['eps_diluted'],

        cash= sec_funds['cash'],
        short_term_investments= sec_funds['short_term_investments'],
        accounts_receivable= sec_funds['accounts_receivable'],
        inventory= sec_funds['inventory'],
        current_assets= sec_funds['current_assets'],
        total_assets= sec_funds['total_assets'],
        current_liabilities= sec_funds['current_liabilities'],
        short_term_debt= sec_funds['short_term_debt'],
        long_term_debt= sec_funds['long_term_debt'],
        total_liabilities= sec_funds['total_liabilities'],
        equity= sec_funds['equity'],

        operating_cash_flow= sec_funds['operating_cash_flow'],
        investing_cash_flow= sec_funds['investing_cash_flow'],
        financing_cash_flow= sec_funds['financing_cash_flow'],
        capital_expenditure= sec_funds['capital_expenditure'],

        shares_outstanding= sec_funds['shares_outstanding'],
        weighted_average_shares= sec_funds['weighted_average_shares_basic'],
        dividends =  sec_funds['dividends'],
        buybacks =  sec_funds['buybacks'],

        current_price = await fund.finn_qoute(symbol=symbol),
        market_cap= metric["marketCapitalization"],
        pe_ratio =  metric['peTTM'],
        ps_ratio =  metric['psTTM'],
        pb_ratio =  metric['pb'],
        ev_ebitda = metric['evEbitdaTTM'],
        roe =  metric['roeRfy'],
        roa =  metric['roaRfy'],
        debt_equity =  f"{metric['totalDebt']}/{metric['totalEquityAnnual']}",

        earnings= metric['peTTM'],
        eps_estimates= yf_data['eps_estimate'],
        revenue_estimates= yf_data['revenue_estimate'],
        earnings_surprise= yf_data['earnings_surprise'],
        revenue_surprise= (sec_funds['revenue'] - yf_data["revenue_estimate"]) / yf_data["revenue_estimate"],
        company_peers =  await fund.company_peers(symbol=symbol),

        macro_gdp= macro['macro_gdp'],
        macro_gdp_growth= macro['macro_gdp_growth'],
        macro_inflation= macro['macro_inflation'],
        macro_interest_rates= macro['macro_interest_rates'],
        macro_unemployment= macro['macro_unemployment'],
        macro_government_debt= macro['macro_government_debt'],
        macro_exchange_rates =  macro['macro_exchange_rates'],
    )


if __name__ == '__main__':
    async def main():
        fund = get_fundamentels(symbol='AAPL')
        print(fund)
    asyncio.run(main())
