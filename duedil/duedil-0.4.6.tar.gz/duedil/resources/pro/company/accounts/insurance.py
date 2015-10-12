from __future__ import unicode_literals

from .... import ProResource


class AccountDetailsInsurance(ProResource):
    attribute_names = [
        'account_status',
        # integer Account status
        'accountant_fees',
        # integer Accountant fees
        'accruals_and_deferred_income',
        # integer Accruals & deferred income
        'accrued_interest_and_rent',
        # integer Accrued interest and rent
        'acquisitions_and_disposals',
        # integer Acqisitions and discposals
        'amortisation_of_intangibles',
        # integer Amortisation of intangibles
        'amounts_owed_to_credit_institutions',
        # integer Debtors arising out of insurance operations
        'amounts_owed_to_group_undertakings',
        # integer Debtors arising out of group undertakings
        'assets_deferred_tax',
        # integer Deferred tax assets
        'assets_held_for_resale',
        # integer Assets held for resale
        'assets_intangible',
        # integer Intangible assets
        'assets_investment',
        # integer Investment asset
        'assets_other',
        # integer Other assets
        'assets_other_intangible',
        # integer Other intangible assets
        'assets_tangible',
        # integer Tangible assets
        'auditor_fees',
        # integer Auditor fees
        'borrowings',
        # integer Borrowings
        'borrowings_due_after',
        # integer Borrowings due after one year
        'borrowings_due_within',
        # integer Borrowings due within one year
        'capital_expenditure',
        # integer Capital expenditure
        'cash_and_bank_and_in_hand',
        # integer Cash at bank and in hand
        'cash_and_cash_equivalents',
        # integer Cash and cash equivalents
        'cash_year_start',
        # integer Cash at start of the year
        'change_in_cash',
        # integer Change in cash
        'company',
        # integer Company registration number
        'consolidated_accounts',
        # integer Consolidated accounts
        'creditors',
        # integer Creditors
        'currency',
        # integer Currency
        'current_tax_recoverable',
        # integer Current tax recoverable
        'debt_securities',
        # integer Debt securities
        'debtors',
        # integer Debtors
        'debtors_arising_out_of_group_undertakings',
        # integer Debtors arising out of group undertakings
        'debtors_arising_out_of_insurance_operations',
        # integer Debtors arising out of insurance operations
        'deferred_acquisition_costs',
        # integer Deferred acquisition costs
        'deposits_received_from_reinsurers',
        # integer Deposits received from reinsurers
        'depreciation_of_tangibles',
        # integer Depreciation of tangibles
        'direct_insurance_operations',
        # integer Direct insurance operations
        'director_fees',
        # integer Director fees
        'director_other',
        # integer Director other
        'director_pensions',
        # integer Director pensions
        'director_social_security',
        # integer Director social security
        'directors_remuneration',
        # integer Directors remuneration
        'discontinued_ops',
        # integer Discontinued ops
        'dividends',
        # integer Dividends
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
        # integer Employee
        'equity_dividends_paid',
        # integer Equity dividends paid
        'exceptional_items',
        # integer Exceptional items
        'exceptional_other_items',
        # integer Exceptional other items
        'exceptional_pandl_on_disposal',
        # integer Exceptional profit/loss on disposal
        'exceptional_pandl_on_reorganisations',
        # integer Exceptional profit/loss on reorganisations
        'exchange_rate_effect',
        # integer Exchange rate effect
        'fee_commission_income',
        # integer Fee & commission income
        'finance',
        # integer Finance
        'finance_costs',
        # integer Finance costs
        'financial_investments_after',
        # integer Financial investments after 12 months
        'financial_investments_within',
        # integer Financial investments within 12 months
        'financing_activities',
        # integer Financing activities
        'gaap_other_appropriations',
        # integer GAAP other appropriations
        'goodwill',
        # integer Goodwill
        'gross_written_premiums',
        # integer Gross written premiums
        'highest_paid_director',
        # integer Highest paid director
        'id',
        # integer ID
        'ifrs_other_appropriations',
        # integer IFRS other appropriations
        'insurance_debtors_and_assets',
        # integer Insurance debtors and assets
        'insurance_debtors_and_assets_settled_after',
        # integer Insurance debtors and assets to be settled after 12 months
        'insurance_debtors_and_assets_settled_within',
        # integer Insurance debtors and assets to be settled within 12 months
        'investing_activities',
        # integer Investing activities
        'investment',
        # integer Investment
        'investment_due_after',
        # integer Investment due after 12 months
        'investment_due_within',
        # integer Investments due within 12 months
        'investment_expenses_and_charges',
        # integer Investment expenses and charges
        'investment_income',
        # integer Investment income
        'investment_property',
        # integer Investment property
        'investments',
        # integer Investments
        'investments_in_group_undertakings',
        # integer Investments in group undertakings
        'land_and_buildings',
        # integer Land and buildings
        'less_income_tax_attributable_to_policyholders_returns',
        # integer Less income tax attributable to policyholders' returns
        'liabilities_current_tax',
        # integer Current tax liabilities
        'liabilities_deferred_tax',
        # integer Deferred tax liabilities
        'liabilities_held_for_sale',
        # integer Liabilities held for sale
        'liabilities_insurance',
        # integer Insurance liabilities
        'liabilities_insurance_settled_within',
        # integer Insurance liabilities to be settled within 12 months
        'liabilities_insurances_settled_after',
        # integer Insurance liabilities to be settled after 12 months
        'liabilities_other_non_insurance',
        # integer Other non-insurance liabilities
        'liabilities_reinsurance',
        # integer Reinsurance liabilities
        'liabilities_reinsurance_settled_after',
        # integer Reinsurance liabilities to be settled after 12 months
        'liabilities_reinsurance_settled_within',
        # integer Reinsurance liabilities to be settled within 12 months
        'loans_after',
        # integer Loans after 12 months
        'loans_and_deposits_with_credit_institutions',
        # integer Loans and deposits with credit institutions
        'loans_within',
        # integer Loans within 12 months
        'management_of_liquid_resources',
        # integer Management of liquid resources
        'minority_interests',
        # integer Minority interests
        'months',
        # integer Months
        'net_change_in_cash',
        # integer Net change in cash
        'net_change_in_provision_for_unearned_premiums',
        # integer Net change in provision for unearned premiums
        'net_operating_expense',
        # integer Net operating expense
        'net_pension_liability',
        # integer Net pensions liability
        'net_premiums_earned',
        # integer Net premiums earned
        'operating_activities',
        # integer Operating activities
        'ordinary_shares',
        # integer Ordinary shares
        'other_audit_costs',
        # integer Other audit costs
        'other_creditors',
        # integer Other creditors
        'other_debtors',
        # integer Other debtors
        'other_investments',
        # integer Other investments
        'other_investments_after',
        # integer Other investments after 12 months
        'other_investments_within',
        # integer Other investments within 12 months
        'other_liabilities',
        # integer Other liabilities
        'other_lt_loans',
        # integer Other long term loans
        'other_operating_income',
        # integer Other operating income
        'other_prepayments_and_accrued_income',
        # integer Other prepayments and accrued income
        'other_reserves',
        # integer Other reserves
        'other_shares',
        # integer Other shares
        'other_technical_income',
        # integer Other technical income
        'outward_reinsurance_premiums',
        # integer Outward reinsurance premiums
        'pandl_revenue_reserve',
        # integer Profit & loss / revenue reserve
        'plant_and_equipment',
        # integer Plant and equipment
        'pre_tax_profit',
        # integer Pre-tax profit
        'preference_shares',
        # integer Preference shares
        'prepayments_and_accrued_income',
        # integer Prepayments and accrued income
        'profit_after_tax',
        # integer Profit after tax
        'profit_attributable_to_minority_investments',
        # integer Profit attributable to minority interests
        'profit_before_tax_attributable_to_shareholders',
        # integer Profit before tax attributable to shareholders
        'profit_from_continuing_operations_after_tax',
        # integer Profit from continuing operations after tax
        'property',
        # integer Property
        'provisions',
        # integer Provisions
        'provisions_for_other_risks_and_charged',
        # integer Provisions for other risks and charges
        'reinsurance_debtors_and_assets',
        # integer Reinsurance debtors and assets
        'reinsurance_debtors_and_assets_settled_after',
        # integer Reinsurance debtors and assets settled after 12 months
        'reinsurance_debtors_and_assets_settled_within',
        # integer Reinsurance debtors and assets settled within 12 months
        'reinsurance_operations',
        # integer Reinsurance operations
        'reinsurers_share_of_technical_provisions',
        # integer Reinsurers share of technical provisions
        'retained_profit',
        # integer Retained profit
        'return_on_investment',
        # integer Return on investment
        'revaluation_reserve',
        # integer Revaluation reserve
        'share_premium',
        # integer Share premium
        'shares_and_other_variable_yield_securities',
        # integer Shares and other variable yield securities
        'statutory_audit_costs',
        # integer Statutory audit costs
        'subordinated_borrowings',
        # integer Subordinated borrowings
        'tax',
        # integer Tax
        'tax_attributable_to_policyholders_returns',
        # integer Tax attributable to policyholders' returns
        'tax_attributable_to_shareholders_profits',
        # integer Tax attributable to shareholders profits
        'tax_expense',
        # integer Tax expense
        'taxation',
        # integer Taxation
        'technical_provisions',
        # integer Technical provisions
        'total_called_issued_capital',
        # integer Total called up / issued capital
        'total_capital_reserves',
        # integer Total capital reserves
        'total_equity_and_reserves',
        # integer Total equity and reserves
        'total_shareholders_funds',
        # integer Total shareholders funds
        'turnover',
        # integer Turnover
        'type',
        # integer Type
        'year_end_cash_equivalents',
        # integer Year end cash equivalents
    ]
