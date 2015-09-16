from decimal import Decimal


number_t = "Number"
boolean_t = "Boolean"
string_t = "String"

type_defaults = {
  number_t: Decimal(0),
  boolean_t: True,
  string_t: ""
}
