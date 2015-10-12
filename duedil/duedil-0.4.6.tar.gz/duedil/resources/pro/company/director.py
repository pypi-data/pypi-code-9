from __future__ import unicode_literals


from ... import ProResource, RelatedResourceMixin


class Director(RelatedResourceMixin, ProResource):

    path = 'directors'

    attribute_names = [
        # 'id',
        # string Director ID
        'last_update',
        # dateTime Date last updated
        'open_directorships_count',
        # integer Number of open directorships
        'open_trading_directorships_count',
        # integer Number of open trading directorships
        'open_trading_director_directorships_count',
        # integer Of which a director
        'open_trading_secretary_directorships_count',
        # integer Of which a secretary
        'closed_directorships_count',
        # integer Number of closed directorships
        'retired_directorships_count',
        # integer Number of retired directorships
        'director_directorships_count',
        # integer Number of directorships (director)
        'open_director_directorships_count',
        # integer Number of open directorships (director)
        'closed_director_directorships_count',
        # integer Number of closed directorships (director)
        'secretary_directorships_count',
        # integer Number of secretary directorships
        'open_secretary_directorships_count',
        # integer Number of open secretary directorships
        'closed_secretary_directorships_count',
        # integer Number of closed secretary directorships
        'retired_secretary_directorships_count',
        # integer Number of retired decretary directorships
        'forename',
        # string Forename
        'surname',
        # string Surname
        'date_of_birth',
        # dateTime Date of Birth
        'directorships_url',
        # string Link to directorships
        'companies_url',
        # string Link to companies
        'director_url',
        # string Link to director profile
        # undocumented:
        'middle_name',
        'title',
        'postal_title',
        'nationality',
        'nation_code',
    ]

    related_resources = {
        'companies': 'resources.pro.company.Company',
        'directorships': 'resources.pro.company.DirectorShip',
    }

    term_filters = [
        "name",  # string
        # This field must be a string that contains the director's name.
        "gender",  # string
        # This term accepts only the value M or F
        "title",  # string
        # View all available titles.
        "nationality",  # string
        # View all available nationalities.
        "secretarial",  # boolean
        # This is a boolean field; the values accepted are true or false
        "corporate",  # boolean
        # This is a boolean field; the values accepted are true or false
        "disqualified",  # string
        # This is a boolean field; the values accepted are true or false
    ]

    range_filters = [
        "age",  # string
        # The age brackets of the director
        "data_of_birth",  # dateTime
        # The date of birth brackets of the director. The data must be in this
        # format MM/DD/YYY
        "gross_profit",  # float
        # Turnover minus the cost of sales. Gross profit doesn't include
        # administrative, financial, or distribution costs.
        "gross_profit_delta_percentage",  # string
        # Movement in gross profit from previous year's filing to latest
        # filing.
        "turnover",  # string
        # The income a company Receives from normal business activities.
        # Internationally known as "revenue".
        "turnover_delta_percentage",  # string
        # Movement in turnover from previous year's filing to latest filing.
        "cost_of_sales",  # string
        # Costs attributable to the production of the goods or supply of
        # services.
        "cost_of_sales_delta_percentage",  # string
        # Movement in cost of sales from previous year's filing to latest
        # filing.
        "depreciation",  # string
        # A decrease in the value of company assets. Depreciation indicates how
        # much of an asset's value has been used up.
        "depreciation_delta_percentage",  # string
        # Movement in depreciation from previous year's filing to latest
        # filing.
        "taxation",  # string
        # Amount set aside for taxation purposes.
        "cash",  # string
        # Included in current assets, cash refers to the amount held in current
        # or deposit bank accounts, and is seen as a highly liquid form of
        # current asset.
        "cash_delta_percentage",  # string
        # Movement in cash from previous year's filing to latest filing.
        "net_worth",  # string
        # The amount by which assets exceed liabilities. Net worth is a concept
        # applicable to businesses as a measure of how much an entity is worth.
        "net_worth_delta_percentage",  # string
        # Movement in net worth from previous year's filing to latest filing.
        "total_assets",  # string
        # The sum of current and long-term assets owned by the company.
        "total_assets_delta_percentage",  # string
        # The change in the total assets value from previous year's filing to
        # latest filing.
        "current_assets",  # string
        # All assets belonging to a company that can be converted easily into
        # cash and are expected to be used (sold or consumed) within a year.
        "current_assets_delta_percentage",  # string
        # The change in the current assets value from the previous year's
        # filing to latest filing.
        "net_assets",  # string
        # Net assets refers to the value of a company's assets minus its
        # liabilities.
        "net_assets_delta_percentage",  # string
        # Percentage change between the latest filing's value and previous
        # filing's value of net assets.
        "total_liabilities",  # string
        # The total of all debts for which a company is liable; includes
        # short-term and long-term liabilities.
        # string
        "total_liabilities_delta_percentage",
        # The change in the value of total liabilities from previous year's
        # filing to latest filing.
    ]
