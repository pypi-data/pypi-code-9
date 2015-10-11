class AbstractFormatter:

  def format_type_error(self, error):
    raise NotImplementedError()

  def format_value_error(self, error):
    raise NotImplementedError()

  def format_min_value_error(self, error):
    raise NotImplementedError()

  def format_max_value_error(self, error):
    raise NotImplementedError()

  def format_remainder_error(self, error):
    raise NotImplementedError()

  def format_pattern_mismatch_error(self, error):
    raise NotImplementedError()

  def format_length_error(self, error):
    raise NotImplementedError()

  def format_min_length_error(self, error):
    raise NotImplementedError()

  def format_max_length_error(self, error):
    raise NotImplementedError()

  def format_index_error(self, error):
    raise NotImplementedError()

  def format_min_occurrence_error(self, error):
    raise NotImplementedError()

  def format_exactly_occurrence_error(self, error):
    raise NotImplementedError()

  def format_missing_key_error(self, error):
    raise NotImplementedError()

  def format_extra_key_error(self, error):
    raise NotImplementedError()

  def format_schema_mismatch_error(self, error):
    raise NotImplementedError()

  def format_single_schema_mismatch_error(self, error):
    raise NotImplementedError()

  def format_enumeration_error(self, error):
    raise NotImplementedError()
