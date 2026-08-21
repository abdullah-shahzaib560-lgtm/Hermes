from hermes.sources.finnhub import FINNHUB
from hermes.core.models.analysis.fundamental import CompanyFundamental

class fundamenatals:

    def __init__(self, api, cache):
        self.finn = FINNHUB(api=api, cache=cache)

    async def profile(
        self,
        symbol: str
    ) -> dict:
        resp = await self.finn.fetch(endpoint='profile', symbol=symbol)
        data = {
            "name": resp['ticker'],
            "exchange": resp['exchange'],
            "currency": resp['currency'],
            "industry": resp['finnhubIndustry'],
            "country": resp['country'],
            "market_cap": resp['marketCapitalization'],
            "shares_outstanding": resp['shareOutstanding']
        }
        return data

    async def metric(
        self,
        symbol: str
    ) -> dict:

        resp = await self.finn.fetch(endpoint='metric', symbol=symbol)
        result = {
            "pe_ratio":         resp['metric']["peTTM"],
            "pb_ratio":         resp['metric']["pb"],
            "ps_ratio":         resp['metric']["psTTM"],
            "dividend_yield":   resp['metric']["currentDividendYieldTTM"],
            "gross_margin":     resp['metric']["grossMarginAnnual"],
            "operating_margin": resp['metric']["operatingMarginAnnual"],
            "net_margin":       resp['metric']["netProfitMarginAnnual"],
            "roe":              resp['metric']["roeRfy"],
            "roa":              resp['metric']["roaRfy"],
            "52WeekHigh":       resp['metric']["52WeekHigh"],
            "52WeekLow":        resp['metric']["52WeekLow"],
            "beta":             resp['metric']["beta"],
        }
        return result

    def compute_eps_ttm(earnings: list) -> float | None:
        if not earnings or len(earnings) < 4:
            return None

        sorted_earnings = sorted(
            earnings,
            key=lambda x: x["period"],
            reverse=True
        )

        last_4 = sorted_earnings[:4]
        eps_ttm = sum(item["actual"] for item in last_4)
        return eps_ttm
    
    async def earnings(self, symbol):
        earnings = await self._req(endpoint='earnings', symbol=symbol)
        epx_ttm = self.compute_eps_ttm(earnings=earnings)


async def fundamentals_pipeline(symbol: str):
    fund = fundamenatals()
    profile = await fund.profile(symbol=symbol)
    metric = await fund.metric(symbol=symbol)

    return CompanyFundamental(
        symbol=symbol,
        name=profile['name'],
        exchange=profile['exchange'],
        currency=profile['currency'],
        sector=profile['sector'],
        industry=profile['industry'],
        country=profile['country'],
        market_cap=profile['market_cap'],
        shares_outstanding=profile['shares_outstanding'],
        pe_ratio=metric['pe_ratio'],
        pb_ratio=metric['pb_ratio'],
        ps_ratio=metric['ps_ratio'],
        dividend_yield=metric['dividend_yield'],
        gross_margin=metric['gross_margin'],
        operating_margin=metric['operating_margin'],
        net_margin=metric['net_margin'],
        roe=metric['roe'],
        roa=metric['roa'],
        
    )
