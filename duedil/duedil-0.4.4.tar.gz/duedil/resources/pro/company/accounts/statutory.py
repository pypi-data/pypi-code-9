from __future__ import unicode_literals

from .... import ProResource


class AccountDetailsStatutory(ProResource):
    attribute_names = [
        'id',
        # string Accounts ID
        'last_update',
        # dateTime Date of last update
        'company',
        # string Company registration number
        'date',
        # string Accounting to date
        'type',
        # string Type of accounts
        'account_status',
        # integer Account status
        'accountants',
        # integer Accountants
        'accounts_format',
        # integer Accounts format
        'auditors',
        # string Auditor name
        'assets_current',
        # integer Current assets
        'assets_net',
        # integer Net assets
        'assets_other_current',
        # integer Other current assets
        'assets_tangible',
        # integer Tangible assets
        'assets_total',
        # integer Total assets
        'assets_total_current',
        # integer Total current assets
        'assets_total_fix',
        # integer Total fixed assets
        'assets_current_delta',
        # integer The change in the current assets value from the previous
        # year's filing to latest filing
        'assets_current_delta_percentage',
        # integer The percentage change in the current assets value from the
        # previous year's filing to latest filing
        'assets_intangible',
        # integer Intangible assets
        'assets_intangible_delta',
        # integer The change in the intangible assets value from the previous
        # year's filing to latest filing
        'assets_intangible_delta_percentage',
        # integer The percentage change in the current assets value from the
        # previous year's filing to latest filing
        'assets_net_delta',
        # integer The change in net assets value from the previous year's
        # filing to latest filing
        'assets_net_delta_percentage',
        # integer The percentage change in net assets value from the previous
        # year's filing to latest filing
        'assets_other_current_delta',
        # integer The change in other assets value from the previous year's
        # filing to latest filing
        'assets_other_current_delta_percentage',
        # integer The percentage change in other assets value from the previous
        # year's filing to latest filing
        'assets_tangible_delta',
        # integer The change in tangible assets value from the previous year's
        # filing to latest filing
        'assets_tangible_delta_percentage',
        # integer The percentage change in tangible assets value from the
        # previous year's filing to latest filing
        'assets_total_current_delta',
        # integer The change in total current assets value from the previous
        # year's filing to latest filing
        'assets_total_current_delta_percentage',
        # integer The percentage change in total current assets value from the
        # previous year's filing to latest filing
        'assets_total_delta',
        # integer The change in total current assets value from the previous
        # year's filing to latest filing
        'assets_total_delta_percentage',
        # integer The percentage change in total current assets value from the
        # previous year's filing to latest filing
        'assets_total_fix_delta',
        # integer The change in total fixed assets value from the previous
        # year's filing to latest filing
        'assets_total_fix_delta_percentage',
        # integer The change in total fixed assets value from the previous
        # year's filing to latest filing
        'audit_fees',
        # integer Audit fees
        'audit_fees_delta',
        # integer The change in audit fees from the previous year's filing
        # to latest filing
        'audit_fees_delta_percentage',
        # integer The percentage change in audit fees from the previous year's
        # filing to latest filing
        'bank_overdraft',
        # integer Bank overdraft
        'bank_overdraft_delta',
        # integer The change in bank overdraft from the previous year's filing
        # to latest filing
        'bank_overdraft_delta_percentage',
        # integer The percentage change in bank overdraft from the previous
        # year's filing to latest filing
        'bank_overdraft_lt_loans_delta',
        # integer The change in bank overdraft & long term loans from the
        # previous year's filing to latest filing
        'bank_overdraft_lt_loans_delta_percentage',
        # integer The percentage change in bank overdraft & long term loans
        # from the previous year's filing to latest filing
        'bank_overdraft_lt_loans',
        # integer Bank overdraft & long term loans
        'capital_employed',
        # integer Capital employed
        'capital_employed_delta',
        # integer The change in total capital employed from the previous year's
        # filing to latest filing
        'capital_employed_delta_percentage',
        # integer The percentage change in total capital employed value from
        # the previous year's filing to latest filing
        'cash',
        # integer Cash
        'cash_delta',
        # integer The change in total cash from the previous year's filing to
        # latest filing
        'cash_delta_percentage',
        # integer The percentage change in total cash value from the previous
        # year's filing to latest filing
        'company',
        # integer Company registration number
        'consolidated',
        # boolean Consolidated accounts (Y/N)
        'contingent_liability',
        # integer Contingent liability
        'contingent_liability_delta',
        # integer The change in contingent liability from the previous year's
        # filing to latest filing
        'contingent_liability_delta_percentage',
        # integer The percentage change in contingent liability from the
        # previous year's filing to latest filing
        'cost_of_sales',
        # integer Cost of sales
        'cost_of_sales_delta',
        # integer The change in cost of sales from the previous year's filing
        # to latest filing
        'cost_of_sales_delta_percentage',
        # integer The percentage change in cost of sales from the previous
        # year's filing to latest filing
        'currency',
        # string Accounts currency
        'debtor_days',
        # integer Debtor days
        'depreciation',
        # integer Depreciation
        'depreciation_delta',
        # integer The change in depreciation from the previous year's filing to
        # latest filing
        'depreciation_delta_percentage',
        # integer The percentage change in depreciation from the previous
        # year's filing to latest filing
        'directors_emoluments_delta',
        # integer The change in directors' emoluments from the previous year's
        # filing to latest filing
        'directors_emoluments_delta_percentage',
        # integer The percentage change in directors' emoluments from the
        # previous year's filing to latest filing
        'directors_emoluments',
        # integer Directors' emoluments
        'dividends_payable',
        # integer Dividends payable
        'dividends_payable_delta',
        # integer The change in dividends payable from the previous year's
        # filing to latest filing
        'dividends_payable_delta_percentage',
        # integer The percentage change in dividends payable from the previous
        # year's filing to latest filing
        'exports',
        # integer Exports
        'exports_delta',
        # integer The change in exports from the previous year's filing to
        # latest filing
        'exports_delta_percentage',
        # integer The percentage change in exports from the previous year's
        # filing to latest filing
        'gross_profit',
        # integer Gross profit
        'gross_profit_delta',
        # integer The change in gross profit from the previous year's filing to
        # latest filing
        'gross_profit_delta_percentage',
        # integer The percentage change in profit from the previous year's
        # filing to latest filing
        'increase_in_cash',
        # integer Increase in cash
        'increase_in_cash_delta',
        # integer The change in increase in cash from the previous year's
        # filing to latest filing
        'increase_in_cash_delta_percentage',
        # integer The percentage change in increase in cash from the previous
        # year's filing to latest filing
        'interest_payments',
        # integer Interest payments
        'interest_payments_delta',
        # integer The change in interest payments from the previous year's
        # filing to latest filing
        'interest_payments_delta_percentage',
        # integer The percentage change in interest payments from the previous
        # year's filing to latest filing
        'joint_auditors',
        # integer Joint auditors
        'liabilities_current',
        # integer Current liabilities
        'liabilities_lt',
        # integer Long term liabilities
        'liabilities_misc_current',
        # integer Miscellaneous current liabilities
        'liabilities_total',
        # integer Total liabilities
        'liabilities_current_delta',
        # integer The change in current liabilities from the previous year's
        # filing to latest filing
        'liabilities_current_delta_percentage',
        # integer The change in current liabilities from the previous year's
        # filing to latest filing
        'liabilities_lt_delta',
        # integer The change in long terms liablilties from the previous year's
        # filing to latest filing
        'liabilities_lt_delta_percentage',
        # integer The percentage change in long term liabilities from the
        # previous year's filing to latest filing
        'liabilities_misc_current_delta',
        # integer The change in miscellaneous current liabilities from the
        # previous year's filing to latest filing
        'liabilities_misc_current_delta_percentage',
        # integer The percentage change in miscellaneous current liabilities
        # from the previous year's filing to latest filing
        'liabilities_total_delta',
        # integer The change in total liabilities from the previous year's
        # filing to latest filing
        'liabilities_total_delta_percentage',
        # integer The percentage change in total liabilities from the previous
        # year's filing to latest filing
        'lt_loans',
        # integer Long term loans
        'lt_loans_delta',
        # integer The change in long term loans from the previous year's filing
        # to latest filing
        'lt_loans_delta_percentage',
        # integer The percentage change in long term loans from the previous
        # year's filing to latest filing
        'months',
        # integer Months included in accounts
        'net_cashflow_before_financing',
        # integer Net cashflow before financing
        'net_cashflow_from_financing',
        # integer Net cashflow from financing
        'net_cashflow_before_financing_delta',
        # integer The change in net cashflow before financing from the previous
        # year's filing to latest filing
        'net_cashflow_before_financing_delta_percentage',
        # integer The percentage change in net cashflow before financing from
        # the previous year's filing to latest filing
        'net_cashflow_from_financing_delta',
        # integer The change in net cashflow from financing from the previous
        # year's filing to latest filing
        'net_cashflow_from_financing_delta_percentage',
        # integer The percentage change in net cashflow from financing from the
        # previous year's filing to latest filing
        'net_worth_delta',
        # integer The change in net worth from the previous year's filing to
        # latest filing
        'net_worth_delta_percentage',
        # integer The change in net worth from the previous year's filing to
        # latest filing
        'net_worth',
        # integer Net worth
        'no_of_employees',
        # integer Number of employees
        'no_of_employees_delta',
        # integer The change in number of employees from the previous year's
        # filing to latest filing
        'no_of_employees_delta_percentage',
        # integer The percentage change in number of employees from the
        # previous year's filing to latest filing
        'operating_profits',
        # integer Operating profits
        'operating_profits_delta',
        # integer The change in operating profits from the previous year's
        # filing to latest filing
        'operating_profits_delta_percentage',
        # integer The percentage change in operating profits from the previous
        # year's filing to latest filing
        'operations_net_cashflow_delta',
        # integer The change in operations net cashflow from the previous
        # year's filing to latest filing
        'operations_net_cashflow_delta_percentage',
        # integer The percentage change operations net cashflow from the
        # previous year's filing to latest filing
        'operations_net_cashflow',
        # integer Net cashflow
        'paid_up_equity',
        # integer Paid-up equity
        'paid_up_equity_delta',
        # integer The change in paid-up equity from the previous year's filing
        # to latest filing
        'paid_up_equity_delta_percentage',
        # integer The percentage change in paid-up equity from the previous
        # year's filing to latest filing
        'pandl_account_reserve',
        # integer Profit & loss account reserve
        'pandl_account_reserve_delta',
        # integer The change in profit & loss account reserve from the previous
        # year's filing to latest filing
        'pandl_account_reserve_delta_percentage',
        # integer The percentage change in profit & loss account reserve from
        # the previous year's filing to latest filing
        'pre_tax_profit',
        # integer Pre-tax profit
        'pre_tax_profit_delta',
        # integer The change in pre-tax profit from the previous year's filing
        # to latest filing
        'pre_tax_profit_delta_percentage',
        # integer The percentage change in pre-tax profit from the previous
        # year's filing to latest filing
        'profit_after_tax',
        # integer Profit after tax
        'profit_after_tax_delta',
        # integer The change in profit after tax from the previous year's
        # filing to latest filing
        'profit_after_tax_delta_percentage',
        # integer The percentage change in profits after tax from the previous
        # year's filing to latest filing
        'qualification_code',
        # integer Qualification codes:
        #    0 = No Adverse Comments;
        #    1 = Exempt from audit;
        #    2 = The audit report contains no adverse comments;
        #    3 = The audit report contains additional comments;
        #    4 = The auditors opinions have been limited by the information
        #        provided to them;
        #    5 = The auditors have been unable to give a full opinion due to a
        #        disagreement over accounting practice;
        #    6 = The audit report states that there is uncertainty concerning
        #        the company being a going concern;
        #    7 = The audit report is qualified on more than one matter or there
        #        is an adverse opinion.
        'retained_profit',
        # integer Retained profit
        'retained_profit_delta',
        # integer The change in retained profit from the previous year's filing
        # to latest filing
        'retained_profit_delta_percentage',
        # integer The percentage change in retained from the previous year's
        # filing to latest filing
        'return_on_assets_ratio',
        # integer Return on assets ratio
        'revaluation_reserve',
        # integer Revaluation reserve
        'revaluation_reserve_delta',
        # integer The change in revaluation reserve from the previous year's
        # filing to latest filing
        'revaluation_reserve_delta_percentage',
        # integer The percentage change in revaluation reserve from the
        # previous year's filing to latest filing
        'shareholder_funds',
        # integer Shareholder funds
        'shareholder_funds_delta',
        # integer The change in shareholder funds from the previous year's
        # filing to latest filing
        'shareholder_funds_delta_percentage',
        # integer The change in shareholder funds from the previous year's
        # filing to latest filing
        'short_term_loans',
        # integer Short term loans
        'short_term_loans_delta',
        # integer The change in short term loans from the previous year's
        # filing to latest filing
        'short_term_loans_delta_percentage',
        # integer The percentage change in short term loans from the previous
        # year's filing to latest filing
        'stock',
        # integer Stock
        'solicitors',
        # integer Solicitors
        'stock_delta',
        # integer The change in stock from the previous year's filing to latest
        # filing
        'stock_delta_percentage',
        # integer The percentage change in stock from the previous year's
        # filing to latest filing
        'sundry_reserves',
        # integer Sundry reserves
        'sundry_reserves_delta',
        # integer The change in sundry reserves from the previous year's filing
        # to latest filing
        'sundry_reserves_delta_percentage',
        # integer The percentage change in sundry reserves from the previous
        # year's filing to latest filing
        'taxation',
        # integer Taxation
        'taxation_delta',
        # integer The change in taxation from the previous year's filing to
        # latest filing
        'taxation_delta_percentage',
        # integer The percentage change in taxation from the previous year's
        # filing to latest filing
        'trade_creditors',
        # integer Trade creditors
        'trade_creditors_delta',
        # integer The change in trade creditors from the previous year's filing
        # to latest filing
        'trade_creditors_delta_percentage',
        # integer The percentage change in trade creditors from the previous
        # year's filing to latest filing
        'turnover',
        # integer Turnover
        'trade_debtors',
        # integer Trade debtors
        'trade_debtors_delta',
        # integer The change in trade debtors from the previous year's filing
        # to latest filing
        'trade_debtors_delta_percentage',
        # integer The percentage change in trade debtors from the previous
        # year's filing to latest filing
        'turnover_delta',
        # integer The change in turnover from the previous year's filing to
        # latest filing
        'turnover_delta_percentage',
        # integer The percentage change in turnover from the previous year's
        # filing to latest filing
        'wages',
        # integer Wages
        'wages_delta',
        # integer The change in wages from the previous year's filing to latest
        # filing
        'wages_delta_percentage',
        # integer The percentage change in wages from the previous year's
        # filing to latest filing
        'working_capital',
        # integer Working capital
        'working_capital_delta',
        # integer The change in working capital from the previous year's filing
        # to latest filing
        'cash_to_current_liabilities_ratio',
        # float Cash to current liabilities ratio
        'cash_to_total_assets_ratio',
        # float Cash to total assets ratio
        'current_ratio',
        # float Current ratio
        'gearing',
        # float Gearing
        'gross_margin_ratio',
        # float Gross margin ratio
        'inventory_turnover_ratio',
        # float Inventory turnover ratio
        'liquidity_ratio',
        # float Liquidity ratio
        'net_profitability',
        # float Net profitability
        'profit_ratio',
        # float Profit ratio
        'retained_profits',
        # integer Retained profits
        'return_on_assets_ratio',
        # float Return on assets ratio
        'return_on_capital_employed',
        # float Return on capital employed
        'debt_to_capital_ratio',
        # float Debt to capital ratio
        'enterprise_value_to_revenue_multiple_ratio',
        # float Enterprise value to revenue multiple ratio
        'working_capital_delta_percentage',
        # integer The percentage change in working capital from the previous
        # year's filing to latest filing
    ]
