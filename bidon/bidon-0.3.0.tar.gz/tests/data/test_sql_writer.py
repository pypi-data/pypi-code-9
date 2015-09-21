import unittest

from bidon.data import SQLWriter


class DataSQLWriterTestCase(unittest.TestCase):
  def setUp(self):
    self.sqlw = SQLWriter("%({0})s", "%s", "{0}::{1}", sort_columns=True)

  def _normalize(self, s, joiner):
    return set(s.split(joiner))

  def test_to_placeholder(self):
    self.assertEqual(self.sqlw.to_placeholder("name"), "%(name)s")
    self.assertEqual(self.sqlw.to_placeholder(None), "%s")
    self.assertEqual(self.sqlw.to_placeholder("name", "int"), "%(name)s::int")
    self.assertEqual(self.sqlw.to_placeholder(None, "citext"), "%s::citext")

  def test_to_tuple(self):
    self.assertEqual(self.sqlw.to_tuple(["a","b","c"]), "(a, b, c)")

  def test_value_comparisons(self):
    values = dict(first_name="Bob", last_name="Smith")
    comps = self.sqlw.value_comparisons(values)
    target = ["first_name = %(first_name)s", "last_name = %(last_name)s"]
    self.assertEqual(set(comps), set(target))

  def test_parse_constraints(self):
    sql, params = self.sqlw.parse_constraints("last_name = 'Smith'")
    self.assertEqual(sql, "last_name = 'Smith'")
    self.assertIsNone(params)
    sql, params = self.sqlw.parse_constraints(dict(last_name="Smith"))
    self.assertEqual(sql, "last_name = %(last_name)s")
    self.assertEqual(params, dict(last_name="Smith"))
    sql, params = self.sqlw.parse_constraints(("last_name = %s and first_name = %s", ["Smith", "John"]))
    self.assertEqual(sql, "last_name = %s and first_name = %s")
    self.assertEqual(params, ["Smith", "John"])
    self.sqlw.sort_columns = False
    values = (("id", 10, " <= "), ("last_name", "Smith"), ("age", (40, 50), "between"), ("first_name", ("John", "Susie"), "in"))
    sql, params = self.sqlw.parse_constraints(values)
    self.assertEqual(sql, "id <= %s and last_name = %s and age between %s and %s and first_name in (%s, %s)")
    self.sqlw.sort_columns = True
    sql, params = self.sqlw.parse_constraints(values)
    self.assertEqual(sql, "age between %s and %s and first_name in (%s, %s) and id <= %s and last_name = %s")
    self.assertEqual(params, [10, "Smith", 40, 50, "John", "Susie"])
    self.assertEqual("last_name is %s", self.sqlw.parse_constraints([("last_name", None)])[0])
    self.assertEqual("last_name is not %s", self.sqlw.parse_constraints([("last_name", None, "!=")])[0])
    self.assertEqual("last_name is not %s", self.sqlw.parse_constraints([("last_name", None, "is not")])[0])
    self.assertEqual("last_name is %(last_name)s", self.sqlw.parse_constraints(dict(last_name=None))[0])
    self.assertEqual("not (schedule is %s)", self.sqlw.parse_constraints([("schedule", None, "not(is)")])[0])
    self.assertEqual("not (schedule is not %s)", self.sqlw.parse_constraints([("schedule", None, "not(is not)")])[0])

  def test_get_find_all_query(self):
    vals = dict(first_name="Trey")
    self.assertEqual(self.sqlw.get_find_all_query("people")[0], "select * from people where 1 = 1")
    self.assertEqual(self.sqlw.get_find_all_query("people", vals)[0], "select * from people where first_name = %(first_name)s")
    self.assertEqual(self.sqlw.get_find_all_query("people", vals, columns="id, first_name")[0], "select id, first_name from people where first_name = %(first_name)s")
    self.assertEqual(self.sqlw.get_find_all_query("people", vals, columns=["id", "first_name"], order_by="last_name desc")[0], "select id, first_name from people where first_name = %(first_name)s order by last_name desc")
