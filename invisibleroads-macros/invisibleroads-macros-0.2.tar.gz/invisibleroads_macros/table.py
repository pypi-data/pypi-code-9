def duplicate_selected_columns(all_columns, selected_columns):
    has_overlap = lambda suffix: set(
        all_columns).intersection(x + suffix for x in selected_columns)
    suffix = '*'
    while has_overlap(suffix):
        suffix += '*'
    return list(all_columns) + [x + suffix for x in selected_columns]
