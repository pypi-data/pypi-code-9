from __future__ import unicode_literals

from .... import ProResource


class AccountDetailsGAAP(ProResource):
    attribute_names = [
        'id',
        # string Accounts ID
        'company',
        # string Company registration number
        'last_update',
        # dateTime Date of last update
        'date',
        # dateTime Accounting to date
        'type',
        # string Type of accounts
        'accountant_fees',
        # string Accountant fees
        'account_status',
        # integer Account status
        'accruals_deferred_income',
        # integer Accruals & deferred income
        'accruals_deferred_income_due',
        # integer Accruals & deferred income due after 1 year
        'acquisitions_and_disposals',
        # string Acquisitions and disposals
        'amortisation_of_intangibles',
        # integer Amortisation of intangibles
        'assets_intangible',
        # integer Intangible assets
        'assets_misc_current',
        # string Current miscellaneous
        'assets_tangible',
        # integer Tangible assets
        'assets_total_current',
        # integer Total current assets
        'assets_total_fixed',
        # integer Total fixed assets
        'auditor_fees',
        # integer Auditor fees
        'bank_interest_payable',
        # integer Bank interest payable
        'bank_interest_receivable',
        # string Bank interest receivable
        'bank_loans',
        # string Bank loans
        'bank_loans_lt',
        # string Long terms bank loans
        'bank_overdraft',
        # string Bank overdraft
        'capital_expenditure',
        # string Capital expenditure
        'cash',
        # integer Cash
        'cash_increase_decrease',
        # string Decrease/increase in cash
        'consolidated',
        # boolean Accounts consolidated (Y/N)
        'cost_of_sales',
        # string Cost of sales
        'creditors',
        # integer Creditors
        'currency',
        # string Accounts currency
        'current_hp_commitments',
        # string Current HP agreements
        'current_lease_commitments',
        # string Current lease commitments
        'debtors',
        # integer Debtors
        'debtors_due',
        # integer Debtors due
        'depreciation_of_tangibles',
        # integer Depreciation of tangibles
        'directors_accounts',
        # string Directors accounts
        'directors_accounts_lt',
        # string Directors long term accounts
        'director_other',
        # string Directors other
        'director_fees',
        # integer Director fees
        'director_pensions',
        # integer Director pensions
        'director_social_security',
        # string Director social security
        'directors_remuneration',
        # integer Directors' remenuration
        'dividends',
        # string Dividends
        'dividends_other',
        # string Dividends other
        'employee_costs',
        # integer Employee costs
        'employee_numbers',
        # integer Employee numbers
        'employee_pensions',
        # integer Employee pensions
        'employee_remuneration',
        # integer Employee remuneration
        'employee_social_security',
        # integer Employee social security
        'employee_other',
        # string Employee other
        'equity_dividends_paid',
        # string Equity dividends paid
        'exceptional_items',
        # string Exceptional items
        'exceptional_other_items',
        # string Exceptional other items
        'exceptional_pandl_on_disposal',
        # string Exceptional profit & loss on disposal
        'exceptional_pandl_on_reorganisations',
        # string Exceptional profit & loss on reorganisations
        'exports',
        # string Exports
        'financing_net_cashflow',
        # string Financing net cashflow
        'group_accounts_lt',
        # integer Group accounts
        'gross_profit',
        # string Gross profit
        'group_accounts',
        # string Group accounts
        'group_debtors',
        # string Group debtors
        'group_interest_receivable',
        # string Group interest receivable
        'highest_paid_director',
        # integer Highest paid director
        'hp_interest_payable',
        # string HP interest payable
        'interest_payable',
        # integer Interest payable
        'interest_receivable',
        # integer Interest receivable
        'investment_and_other',
        # integer Interest and other
        'lease_interest_payable',
        # string Lease interest payable
        'liabilities_deferred_tax',
        # string Deferred tax liabilities
        'liabilities_current_tax',
        # integer Current tax liabilities
        'liabilities_other_current',
        # integer Other current liabilities
        'liabilities_other_lt',
        # integer Other long term liabilities
        'liabilities_total_current',
        # integer Total current liabilities
        'liabilities_total_lt',
        # integer Total long term liabilities
        'liabilities_total_other_current',
        # integer Total other current liabilities
        'liabilities_total_other_non_current',
        # integer Total other non current liabilities
        'management_of_liquid_resources',
        # string Management of liquid resources
        'minority_interests',
        # string Minority interests
        'minority_interests_profit',
        # string Minority interests profit
        'misc_debtors',
        # integer Miscellaneous debtors
        'months',
        # integer Months included in accounts
        'net_operations_cashflow',
        # string Net operations cashflow
        'net_pension_liability',
        # string Net pension liability
        'non_current_hp_commitments',
        # string Non current HP commitments
        'non_current_lease_commitments',
        # string Non current lease commitments
        'operating_profit',
        # integer Operating profit
        'ordinary_shares',
        # integer Ordinary shares
        'other_audit_costs',
        # integer Other audit costs
        'other_interest_payable',
        # integer Other interest payable
        'other_loans_lt',
        # integer Other long term loans
        'other_provisions',
        # integer Other provisions
        'other_reserves',
        # integer Other reserves
        'other_appropriations',
        # string Other appropriations
        'other_interest_receivable',
        # string Other interest receivable
        'other_shares',
        # string Other shares
        'other_st_loans',
        # string Other short term loans
        'pandl_revenue_reserve',
        # integer P&L revenue reserve
        'pre_tax_profit',
        # integer Pre-tax profit
        'preference_shares',
        # string Preference shares
        'profit_after_tax',
        # integer Profit after tax
        'retained_profit',
        # integer Retained profit
        'return_on_investment',
        # string Return on investment
        'revaluation_reserve',
        # string Revaluation reserve
        'statutory_audit_costs',
        # integer Statutory audit costs
        'stocks_and_work_in_progress',
        # integer Stocks and work in progress
        'tax',
        # integer Tax
        'taxation',
        # string Taxation
        'total_called_issued_capital',
        # integer Total called issued capital
        'total_lt_loans',
        # integer Total long term loans
        'total_non_current_hp_lease_commitments',
        # string Total non-current HP lease commitments
        'total_provisions',
        # integer Total provisions
        'total_shareholders_funds',
        # integer Total shareholders' funds
        'trade_creditors',
        # integer Trade creditors
        'trade_debtors',
        # integer Trade debtors
        'turnover',
        # integer Turnover
    ]
