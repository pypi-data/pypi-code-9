import unittest
from uuid import uuid4

from bidon.data import transaction, autocommit, DataAccess

from tests import get_data_access, TEST_CALLPROC, TEST_ROWCOUNT


def rand():
  return str(uuid4())


class DataDataAccessTestCase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.dab = get_data_access()
    cls.dab.open()

  @classmethod
  def tearDownClass(cls):
    cls.dab.rollback()
    cls.dab.close()

  def test_execute(self):
    cr = self.dab.execute("select * from people where first_name = 'Yours'")
    r = cr.fetchone()
    self.assertEqual(r.last_name, "Truly")
    if TEST_ROWCOUNT:
      self.assertNotEqual(self.dab.row_count, -1)

  def test_callproc(self):
    if not TEST_CALLPROC: return
    cr, params = self.dab.callproc("test_proc1", (11, "yours"))
    rec = cr.fetchone()
    self.assertEqual(rec.first_name_p, "Yours")
    self.assertEqual(rec.last_name_p, "Truly")
    cr, params = self.dab.callproc("test_proc3", (11, 4))
    v = self.dab.get_scalar(cr)
    self.assertEqual(v, True)
    cr, params = self.dab.callproc("test_proc3", (11, 99))
    v = self.dab.get_scalar(cr)
    self.assertEqual(v, False)

  def test_find(self):
    rec = self.dab.find("people", dict(first_name="Yours"))
    self.assertEqual(rec.last_name, "Truly")
    rec = self.dab.find("people", dict(first_name="Ahab"))
    self.assertIsNone(rec)
    rec = self.dab.find("people", "first_name='Yours'")
    self.assertEqual(rec.last_name, "Truly")
    rec = self.dab.find("people", [("first_name", "Yours")])
    self.assertEqual(rec.last_name, "Truly")
    rec = self.dab.find("people", ("first_name = {0}".format(self.dab.core.sql_writer.to_placeholder(None)), ("Yours", )))
    self.assertEqual(rec.last_name, "Truly")

  def test_find_all(self):
    peeps = list(self.dab.find_all("people", dict(last_name="Michaels"), columns="first_name", order_by="first_name"))
    fns = [i.first_name for i in peeps]
    self.assertEqual(fns, ["Anthony", "Diamond"])
    peeps = list(self.dab.find_all("people", "id >= 10"))
    self.assertEqual(2, len(peeps))
    peeps = list(self.dab.find_all("people", [("id", 11)]))
    self.assertEqual(peeps[0].last_name, "Truly")
    peeps = list(self.dab.find_all("people", [("id", 10, ">=")]))
    self.assertEqual(2, len(peeps))
    peeps = list(self.dab.find_all("people", [("last_name", ("Truly", "Michaels"), "in")]))
    self.assertEqual(3, len(peeps))
    peeps = list(self.dab.find_all("people", [("id", (1, 5), "between")]))
    self.assertEqual(5, len(peeps))
    peeps = list(self.dab.find_all("people", order_by="id", limiting=(5, 0)))
    self.assertEqual(5, len(peeps))
    self.assertEqual([1, 2, 3, 4, 5], [p.id for p in peeps])
    peeps = list(self.dab.find_all("people", order_by="id", limiting=(5, 5)))
    self.assertEqual([6, 7, 8, 9, 10], [p.id for p in peeps])

  def test_page(self):
    peeps, count = self.dab.page("people", (0, 4), order_by="id")
    self.assertEqual(count, 11)
    self.assertEqual([1, 2, 3, 4], [p.id for p in peeps])
    peeps, count = self.dab.page("people", (1, 4), order_by="id")
    self.assertEqual(count, 11)
    self.assertEqual([5, 6, 7, 8], [p.id for p in peeps])

  def test_update(self):
    pid = 11
    da = self.dab

    def fp(id=pid):
      return da.find("people", dict(id=id))

    def trc(n=1):
      if TEST_ROWCOUNT:
        self.assertEqual(da.row_count, n)

    da.update("people", dict(last_name="Smith"), dict(id=pid))
    self.assertEqual(fp().last_name, "Smith")
    da.rollback()

    da.update("people", dict(last_name="Smith"), "id={0}".format(pid))
    trc()
    self.assertEqual(fp().last_name, "Smith")
    da.rollback()

    da.update("people", "last_name='Smith'", dict(id=pid))
    trc()
    self.assertEqual(fp().last_name, "Smith")
    da.rollback()

    da.update("people", "last_name='Smith'", "id={0}".format(pid))
    trc()
    self.assertEqual(fp().last_name, "Smith")
    da.rollback()

    da.update("people", "last_name='TrulyTruly'", [("id", (5, 6, 7, 11), "in")])
    trc(4)
    self.assertEqual(fp().last_name, "TrulyTruly")
    da.rollback()

    da.update("people", [("last_name", "Smith")], "id={0}".format(pid))
    trc()
    self.assertEqual(fp().last_name, "Smith")
    da.rollback()

    da.update("people", "last_name='Smith', first_name='Wotcha'", [("id", pid)])
    trc()
    rec = fp()
    self.assertEqual((rec.last_name, rec.first_name), ("Smith", "Wotcha"))
    da.rollback()

    da.update("people", [("last_name", "Smith")], [("id", 5, " <= ")])
    trc(5)
    rec = fp(1)
    self.assertEqual((rec.last_name, rec.id), ("Smith", 1))
    da.rollback()

    tc = dict(id=1)
    da.update("things", dict(other="something"), tc)
    self.assertEqual(da.find("things", tc).other, "something")
    da.update("things", dict(other=None), tc)
    self.assertIsNone(da.find("things", tc).other)
    da.update("things", dict(other="something"), tc)
    da.update("things", [("other", None)], [("id", tc["id"])])
    self.assertIsNone(da.find("things", tc).other)
    da.rollback()

    self.assertRaises(Exception, lambda: self.update("people", dict(last_name="Smith"), [("id", 5, "<=")]))

  def test_count(self):
    self.assertEqual(self.dab.count("people"), 11)

  def test_insert(self):
    da = self.dab
    da.insert("people", dict(first_name="A", last_name="B", age=55))
    self.assertEqual(da.count("people"), 12)
    da.rollback()

    da.insert("people", (("first_name", "A"), ("last_name", "B"), ("Age", 83)))
    self.assertEqual(da.count("people"), 12)
    da.rollback()

  def test_delete(self):
    da = self.dab
    da.delete("people", dict(id=11))
    self.assertEqual(da.count("people"), 10)
    da.rollback()

  def test_get_scalar(self):
    cr = self.dab.find_all("people", dict(id=11), columns="first_name")
    first_name = self.dab.get_scalar(cr)
    self.assertEqual(first_name, "Yours")

  def test_autocommit(self):
    da1 = get_data_access().open()
    da2 = get_data_access().open()

    da1.autocommit = True
    cnst1 = dict(first_name=rand(), last_name=rand(), age=1)
    da1.insert("people", cnst1)
    self.assertEqual(da2.find("people", cnst1).first_name, cnst1["first_name"])

    da1.autocommit = False
    cnst2 = dict(first_name=rand(), last_name=rand(), age=2)
    da1.insert("people", cnst2)
    self.assertIsNotNone(da1.find("people", cnst2))
    self.assertIsNone(da2.find("people", cnst2))

    da1.rollback()
    da1.delete("people", cnst1)
    da1.commit()
    self.assertEqual(da1.count("people"), 11)

  def test_transaction_contextmanager(self):
    da1 = get_data_access().open()
    da2 = get_data_access().open()
    da1.autocommit = False
    cnst = dict(first_name=rand(), last_name=rand(), age=3)
    with transaction(da1) as da:
      self.assertIsInstance(da, DataAccess)
    with transaction(da1):
      da1.insert("people", cnst)
    self.assertEqual(da2.find("people", cnst).first_name, cnst["first_name"])
    with transaction(da1):
      da1.delete("people", cnst)
    da1.autocommit = True
    self.assertEqual(da1.count("people"), 11)
    try:
      with transaction(da1):
        da1.insert("people", cnst)
        raise Exception()
    except Exception as ex:
      pass
    finally:
      self.assertIsNone(da1.find("people", cnst))

  def test_autocommit_contextmanager(self):
    da = get_data_access().open(False)
    cnst = dict(first_name=rand(), last_name=rand(), age=3)
    with transaction(da):
      with autocommit(da):
        da.insert("people", cnst)
        # Rollback should have no effect
        da.rollback()
    self.assertEqual(da.find("people", cnst).first_name, cnst["first_name"])
    da.delete("people", cnst)
    da.commit()
