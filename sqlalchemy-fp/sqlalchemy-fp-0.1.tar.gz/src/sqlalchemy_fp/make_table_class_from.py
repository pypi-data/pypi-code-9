from pyramda import curry


@curry
def make_table_class_from(base_table_class, class_name, table_name):
    return type(class_name, (base_table_class,), {"__tablename__": table_name})
