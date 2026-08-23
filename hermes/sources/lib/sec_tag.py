SEC_TAG_MAP = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
        "Revenues",
    ],
    "cost_of_revenue": [
        "CostOfRevenue",
        "CostOfGoodsAndServicesSold",
    ],
    "gross_profit": ["GrossProfit"],
    "operating_expenses": ["OperatingExpenses"],
    "operating_income": ["OperatingIncomeLoss"],
    "interest_expense": ["InterestExpenseNonOperating"],
    "pretax_income": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"
    ],
    "income_tax_expense": ["IncomeTaxExpenseBenefit"],
    "net_income": ["NetIncomeLoss"],
    "eps_basic": ["EarningsPerShareBasic"],
    "eps_diluted": ["EarningsPerShareDiluted"],

    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "short_term_investments": ["ShortTermInvestments", "MarketableSecuritiesCurrent"],
    "accounts_receivable": ["AccountsReceivableNetCurrent"],
    "inventory": ["InventoryNet"],
    "current_assets": ["AssetsCurrent"],
    "total_assets": ["Assets"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "short_term_debt": ["ShortTermDebtCurrent", "LongTermDebtCurrent"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "total_liabilities": ["Liabilities"],
    "equity": ["StockholdersEquity"],

    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "investing_cash_flow": ["NetCashProvidedByUsedInInvestingActivities"],
    "financing_cash_flow": ["NetCashProvidedByUsedInFinancingActivities"],
    "capital_expenditure": ["PaymentsToAcquirePropertyPlantAndEquipment"],

    "shares_outstanding": ["EntityCommonStockSharesOutstanding"],
    "weighted_average_shares_basic": ["WeightedAverageNumberOfSharesOutstandingBasic"],
    "weighted_average_shares_diluted": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
    "dividends": ["PaymentsOfDividends"],
    "buybacks": ["PaymentsForRepurchaseOfCommonStock"],
}
