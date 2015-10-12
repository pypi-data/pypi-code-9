from __future__ import unicode_literals

from .... import ProResource


class AccountDetailsIFRS(ProResource):
    attribute_names = [
        'id',
        # string Accounts ID
        'last_update',
        # dateTime Date of last update
        'date',
        # dateTime Accounting to date
        'type',
        # string Type of accounts
        'account_status',
        # integer Account status
        'accountant_fees',
        # integer Accountant fees
        'accruals_deferred_income',
        # integer Accruals & deferred income
        'accruals_deferred_income_due',
        # integer Accruals & deferred income due
        'amortisation_of_intangibles',
        # integer Amortisation of intangibles
        'assets_financial',
        # integer Financial assets
        'assets_financial_current',
        # integer Current financial assets
        'assets_intangible',
        # integer Intangible assets
        'assets_investment',
        # integer Investments
        'assets_other_current',
        # integer Other current assets
        'assets_other_non_current',
        # integer Other non-current assets
        'assets_tangible',
        # integer Tangible assets
        'assets_total_current',
        # integer Total current assets
        'assets_total_non_current',
        # integer Total non-current assets
        'auditor_fees',
        # integer Auditor fees
        'bank_interest_payable',
        # integer Interest payable
        'bank_interest_receivable',
        # integer Interest receivable
        'bank_loan',
        # integer Bank loan
        'bank_overdraft',
        # integer Bank overdraft
        'cash_equivalents',
        # integer Cash equivalents
        'cash_year_start',
        # integer Cash, year start
        'change_in_cash',
        # boolean Change in cash
        'company',
        # integer Company registration number
        'consolidated',
        # boolean Accounts consolidated (Y/N)
        'cost_of_sales',
        # integer Cost of sales
        'currency',
        # string Accounts currency
        'current_grants',
        # integer Current grant
        'current_hp_commitments',
        # integer Current HP lease commitments
        'current_lease_commitments',
        # integer Current lease commitments
        'debtors_due_after',
        # integer Debtors due after one year
        'depreciation_of_tangibles',
        # integer Depreciation of tangibles
        'director_fees',
        # integer Director fees
        'director_other',
        # integer Director other
        'director_pensions',
        # integer Director pensions
        'director_social_security',
        # integer Director social security
        'directors_accounts',
        # integer Directors' accounts
        'directors_remuneration',
        # integer Directors' remuneration
        'dividends_paid',
        # integer Dividends paid
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
        'exceptional_items',
        # integer Exceptional items
        'exceptional_other_items',
        # integer Exceptional other items
        'exceptional_pandl_on_acquisition',
        # integer Exceptional profit & loss on acquisition
        'exceptional_pandl_on_reorganisations',
        # integer Exceptional profit & loss on reorganisations
        'exchange_rate_effect',
        # integer Exchange rate effect
        'exports',
        # integer Exports
        'financing_activities',
        # integer Financing activities
        'finished_goods',
        # integer Finished goods
        'gross_profit',
        # integer Gross profit
        'group_accounts',
        # integer Group accounts
        'group_accounts_payable',
        # integer Group accounts payable
        'group_debtors',
        # integer Group debtors
        'group_interest_receivable',
        # integer Group interest receivable
        'highest_paid_director',
        # integer Highest paid director
        'hp_interest_payable',
        # integer HP interest payable
        'interest_bearing_loans',
        # integer Interest bearing loans
        'interest_payable',
        # integer Interest payable
        'interest_receivable',
        # integer Interest receivable
        'inventories',
        # integer Inventories
        'investing_activities',
        # integer Investing activities
        'lease_interest_payable',
        # integer Lease interest payable
        'liabilities_current_resale',
        # integer Current resale liabilities
        'liabilities_non_current_resale',
        # integer Non-current resale liabilities
        'liabilities_other_current',
        # integer Other non-current liabilities
        'liabilities_current_financial',
        # integer Current financial liabilities
        'liabilities_current_tax',
        # integer Current tax liabilities
        'liabilities_deferred_tax',
        # integer Deferred tax liabilities
        'liabilities_non_current_financial',
        # integer Non current financial liabilities
        'liabilities_other_current_financial',
        # integer Other current financial liabilities
        'liabilities_other_non_current_financial',
        # integer Other non current financial liabilities
        'liabilities_pension',
        # integer Pension liabilities
        'liabilities_total_current',
        # integer Total current liabilities
        'liabilities_total_non_current',
        # integer Total non current liabilities
        'liabilities_total_other_current',
        # integer Total other current liabilities
        'liabilities_total_other_non_current',
        # integer Total other non current liabilities
        'minority_interests',
        # integer Minority interests
        'minority_interests_profit',
        # integer Minority interests profit
        'misc_debtors',
        # integer Miscellaneous debtors
        'months',
        # integer Month included in accounts
        'net_change_in_cash',
        # integer Net change in cash
        'non_current_lease_commitments',
        # integer Non current lease commitments
        'non_current_other_payables',
        # integer Non current other payables
        'operating_activities',
        # integer Operating activities
        'non_current_directors_loans',
        # integer Non-current director's loans
        'non_current_grants',
        # integer Non-current grants
        'non_current_group_accounts_payable',
        # integer Non-current group accounts payable
        'non_current_group_loans',
        # integer Non-current group loans
        'non_current_hp_commitments',
        # integer Non-current HP agreements
        'non_current_trade_payables',
        # integer Non-current trade payables
        'operating_profit',
        # integer Operating profit
        'operations_loss',
        # integer Operations loss
        'ordinary_shares',
        # integer Ordinary shares
        'other_audit_costs',
        # integer Other audit costs
        'other_payables',
        # integer Other payables
        'other_provisions',
        # integer Other provisions
        'other_receivables',
        # integer Other receivables
        'other_reserves',
        # integer Other reserves
        'other_appropriations',
        # integer Other appropriations
        'other_interest_payable',
        # integer Other interest payable
        'other_interest_receivable',
        # integer Other interest receivable
        'other_shares',
        # integer Other shares
        'pandl_revenue_reserve',
        # integer P&L revenue reserve
        'pre_tax_profit',
        # integer Pre-tax profit
        'preference_shares',
        # integer Preference shares
        'profit_after_tax',
        # integer Profit after tax
        'provisions',
        # integer Provisions
        'provisions_charges',
        # integer Provisions charges
        'raw_materials',
        # integer Raw materials
        'retained_profit',
        # integer Retained profit
        'revaluation_reserve',
        # integer Revaluation reserve
        'short_term_loans',
        # integer Short term loans
        'statutory_audit_costs',
        # integer Statutory audit costs
        'tax',
        # integer Tax
        'total_called_issued_capital',
        # integer Total called issued capital
        'total_shareholder_funds',
        # integer Total shareholder funds
        'trade_creditors',
        # integer Trade creditors
        'trade_debtors',
        # integer Trade debtors
        'trade_other_payables',
        # integer Trade other payables
        'turnover',
        # integer Turnover
        'work_in_progress',
        # integer Work in progress
        'year_end_cash_equivalents',
        # integer Year end cash equivalents
    ]
