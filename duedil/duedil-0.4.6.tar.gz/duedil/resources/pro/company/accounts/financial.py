from __future__ import unicode_literals

from .... import ProResource


class AccountDetailsFinancial(ProResource):
    attribute_names = [
        'id',
        # string Accounts ID
        'last_update',
        # dateTime Date of last update
        'date',
        # dateTime Accounting to date
        'type',
        # string Accounts type
        'account_status',
        # integer Accounts status
        'accountant_fees',
        # integer Accountant fees
        'acquisitions_and_disposals',
        # integer Acquisitions and disposals
        'accruals_deferred_income',
        # integer Accruals & deferred income
        'amortisation_of_tangibles',
        # integer Amortisation of tangibles
        'assets_available_for_sale_financial',
        # integer Financial assets available for sale
        'assets_deferred_tax',
        # integer Deferred tax assets
        'assets_financial',
        # integer Financial assets
        'assets_financial_due_after',
        # integer Financial assets due after 12 months
        'assets_financial_due_width',
        # integer Financial assets due within 12 months
        'assets_other_due_after',
        # integer Other assets due after 12 months
        'assets_trading',
        # integer Trading assets
        'assets_intangible',
        # integer Intangible assets
        'assets_investment',
        # integer Investment assets
        'assets_misc_current',
        # integer Miscellaneous current assets
        'assets_other',
        # integer Other assets
        'assets_other_due_within',
        # integer Other assets due within 1 year
        'assets_other_intangible',
        # integer Other intangible assets
        'bank_loan',
        # integer Bank loan
        'bank_overdraft',
        # integer Bank overdraft
        'capital_expenditure',
        # integer Capital expenditure
        'commercial_assets_tangible',
        # integer Tangible commercial assets
        'company',
        # integer Company registration numbers
        'creditors',
        # integer Creditors
        'customer_accounts_due_after',
        # integer Customer accounts due after 12 months
        'financial_assets_tangible',
        # integer Tangible financial assets
        'assets_total_current',
        # integer Total current assets
        'assets_total_fixed',
        # integer Total fixed assets
        'auditor_fees',
        # integer Auditor fees
        'cash',
        # integer Cash
        'cash_at_central_banks',
        # integer Cash at central banks
        'cash_year_start',
        # integer Cash year start
        'change_in_cash',
        # integer Change in cash
        'consolidated_accounts',
        # boolean Accounts consolidated (Y/N)
        'currency',
        # string Accounts currency
        'customer_accounts',
        # integer Customer accounts
        'customer_accounts_due_within',
        # integer Customer accounts due within 1 year
        'debt_securities',
        # integer Debt securities
        'debt_securities_due_after',
        # integer Debt securities due after one year
        'debt_securities_due_within',
        # integer Debt securities due within one year
        'debt_securities_in_issue',
        # integer Debt securities in issue
        'debt_securities_in_issue_due_after',
        # integer Debt securities in issue due after 12 months
        'debt_securities_in_issue_due_within',
        # integer Debt securities in issue due within 12 months
        'debtors',
        # integer Debtors
        'debtors_due_after',
        # integer Debtors due after 12 months
        'deposits_by_banks',
        # integer Deposits by banks
        'deposits_by_banks_due_after',
        # integer Deposits by banks due after 1 year
        'deposits_by_banks_due_within',
        # integer Deposits by banks due within 1 year
        'depreciation_of_tangibles',
        # integer Depreciation of tangibles
        'derivative_financial_instruments',
        # integer Derivative financial instruments
        'derivatives',
        # integer Derivatives
        'derivatives_due_after',
        # integer Derivatives due after 12 months
        'derivatives_due_within',
        # integer Derivatives due within 12 months
        'director_other',
        # integer Director other
        'director_pensions',
        # integer Director pensions
        'director_social_security',
        # integer Director social security
        'directors_accounts',
        # integer Directors accounts
        'director_fees',
        # integer Director fees
        'directors_remuneration',
        # integer Directors' remuneration
        'dividends',
        # integer Dividends
        'dividends_other',
        # integer Other dividends
        'employee_costs',
        # integer Employee costs
        'employee_numbers',
        # integer Employee numbers
        'employee_other',
        # integer Employee other
        'employee_pensions',
        # integer Employee pensions
        'employee_remuneration',
        # integer Employee remuneration
        'employee_social_security',
        # integer Employee social security
        'equity_dividends_paid',
        # integer Equity dividends paid
        'equity_shares',
        # integer Equity shares
        'exceptional_items',
        # integer Exceptional items
        'exceptional_other_items',
        # integer Exceptional other items
        'exceptional_pandl_on_disposal',
        # integer Exceptional profit & loss on disposal
        'exceptional_pandl_on_reorganisations',
        # integer Exceptional profit & loss on reorganisations
        'exchange_rate_effect',
        # integer Exchange rate effect
        'fees_and_commission_expense',
        # integer Fees & commission expense
        'fees_and_commission_income',
        # integer Fees & commission income
        'financing_activities',
        # integer Financing activities
        'goodwill',
        # integer Goodwill
        'group_accounts',
        # integer Group accounts
        'group_debtors',
        # integer Group debtors
        'highest_paid_director',
        # integer Highest paid director
        'hp_commitments',
        # integer HP commitments
        'interest_and_similar_expense',
        # integer Interest & similar expense
        'interest_and_similar_income',
        # integer Interest & similar income
        'investing_activities',
        # integer Investing activities
        'investment_and_other',
        # integer Investment & other
        'investment_property',
        # integer Investment property
        'items_in_course_of_collection',
        # integer Items in course of collection
        'items_in_course_of_transmission',
        # integer Items in course of transmission
        'lease_commitments',
        # integer Lease commitments
        'liabilities_current_tax',
        # integer Current tax liabilities
        'liabilities_deferred_tax',
        # integer Deferred tax liabilities
        'liabilities_financial',
        # integer Financial liablities
        'liabilities_financial_due_after',
        # integer Financial liabilities due after 12 months
        'liabilities_financial_due_within',
        # integer Financial liabilities due within 12 months
        'liabilities_insurance',
        # integer Insurance liabilities
        'liabilities_other_due_after',
        # integer Other liabilities due after one year
        'liabilities_other_provisions',
        # integer Liabilities - other provisions
        'liabilities_subordinated_due_after',
        # integer Subordinated liabilities due after one year
        'liabilities_trading',
        # integer Trading liabilities
        'liabilities_other',
        # integer Other liabilities
        'liabilities_other_due_within',
        # integer Other Liabilities due within 1 year
        'liabilities_subordinated',
        # integer Subordinated liabilities
        'liabilities_subordinated_due_within',
        # integer Subordinated Liabilities due within 1 year
        'loans_and_advances_to_banks',
        # integer Loans & advances to banks
        'loans_and_advances_to_banks_due_after',
        # integer Loans & advances to banks due after 1 year
        'loans_and_advances_to_banks_due_within',
        # integer Loans & advances to banks due within 1 year
        'loans_and_advances_to_customers',
        # integer Loans & advances to customers
        'loans_and_advances_to_customers_due_after',
        # integer Loans & advances to customers due after 1 year
        'loans_and_advances_to_customers_due_within',
        # integer Loans & advances to customers due within 1 year
        'lt_bank_loans',
        # integer Long term bank loans
        'lt_directors_accounts',
        # integer Long term directors accounts
        'lt_group_accounts',
        # integer Long term group accounts
        'lt_hp_commitments',
        # integer Long term HP commitments
        'lt_lease_commitments',
        # integer Long term lease commitments
        'lt_loans',
        # integer Long term loans
        'lt_other_loans_finance',
        # integer Other long term finance loans
        'lt_total_accruals_deferred_income',
        # integer Long term total accruals deferred income
        'lt_total_hp_lease_commitments',
        # integer Long term total HP lease commitments
        'lt_total_liabilities',
        # integer Long term total liabilities
        'management_of_liquid_resources',
        # integer Management of liquid resources
        'minority_interests',
        # integer Minority interests
        'minority_interests_profit',
        # integer Minority interests profit
        'misc_debtors',
        # integer Miscellaneous debtors
        'misc_liabilities',
        # integer Miscellaneous liabilities
        'months',
        # integer Months included in accounts
        'net_cashflow_from_financing',
        # integer Net cashflow from financing
        'net_change_in_cash',
        # integer Net change in cash
        'net_fees_and_commission_income',
        # integer Net fees & commission income
        'net_interest_income',
        # integer Net interest income
        'net_pension_liability',
        # integer Net pension liability
        'net_tax_paid',
        # integer Net tax paid
        'net_trading_income',
        # integer Net trading income
        'operating_activities',
        # integer Operating activities
        'operating_expenses',
        # integer Operating expenses
        'operating_profit',
        # integer Operating profit
        'ordinary_shares',
        # integer Ordinary shares
        'other_audit_costs',
        # integer Other audit costs
        'other_income',
        # integer Other income
        'other_reserves',
        # integer Other reserves
        'other_appropriations',
        # integer Other appropriations
        'other_current_liability',
        # integer Other current liability
        'other_lt_liabilities',
        # integer Other long term liabilities
        'other_provisions_for_liabilities',
        # integer Other provisions for liabilities
        'other_shares',
        # integer Other shares
        'other_st_loans',
        # integer Other short term loans
        'pandl_revenue_reserve',
        # integer P&L revenue reserve
        'pre_tax_profit',
        # integer Pre-tax profit
        'preference_shares',
        # integer Preference shares
        'prepayments_accrued_income',
        # integer Prepayments & accrued income
        'profit_after_tax',
        # integer Profit after tax
        'retained_profit',
        # integer Retained profit
        'return_on_investments',
        # integer Return on investments
        'revaluation_reserve',
        # integer Revaluation reserve
        'share_premium_account',
        # integer Share premium account
        'share_profit_in_ventures',
        # integer Share profit in ventures
        'statutory_audit_costs',
        # integer Statutory audit costs
        'stocks_work_in_progress',
        # integer Stocks work in progress
        'tax',
        # integer Tax
        'total_current_liabilities',
        # integer Total current liabilities
        'total_current_liabilities',
        # integer Total long term liabilities
        'total_operating_income',
        # integer Total operating income
        'total_shareholders_funds',
        # integer Total shareholders' funds
        'total_called_issued_capital',
        # integer Total called issued capital
        'total_lt_liabilities',
        # integer Total long term liabilities
        'total_other_creditors',
        # integer Total other creditors
        'total_provisions',
        # integer Total provisions
        'trade_creditors',
        # integer Trade creditors
        'trade_debtors',
        # integer Trade debtors
        'treasury_other_bills',
        # integer Other treasury bills
        'year_end_cash_equivalents',
        # integer Year end cash equivalents
    ]
