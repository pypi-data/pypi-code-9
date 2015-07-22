# -*- coding: utf-8 -*-
# This file is a part of the AnyBlok project
#
#    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import DBTestCase
from anyblok import Declarations
from anyblok.field import FieldException
from anyblok.column import Integer, String
from anyblok.relationship import One2One
from sqlalchemy import ForeignKeyConstraint

register = Declarations.register
Model = Declarations.Model


def _complete_one2one(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)
        street = String()
        zip = String()
        city = String()

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address = One2One(model=Model.Address,
                          remote_columns="id", column_names="id_of_address",
                          backref="person", nullable=False)


def _minimum_one2one(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address = One2One(model=Model.Address, backref="person")


def _one2one_with_str_method(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address = One2One(model="Model.Address", backref="person")


def _minimum_one2one_without_backref(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address = One2One(model=Model.Address)


def _minimum_one2one_with_one2many(**kwargs):

    @register(Model)
    class Address:

        id = Integer(primary_key=True)

    @register(Model)
    class Person:

        name = String(primary_key=True)
        address = One2One(model=Model.Address,
                          backref="person", one2many="persons")


class TestOne2One(DBTestCase):

    def test_complete_one2one(self):
        registry = self.init_registry(_complete_one2one)
        self.assertTrue(hasattr(registry.Person, 'address'))
        self.assertTrue(hasattr(registry.Person, 'id_of_address'))
        address = registry.Address.insert(
            street='14-16 rue soleillet', zip='75020', city='Paris')
        person = registry.Person.insert(
            name="Jean-sébastien SUZANNE", address=address)

        self.assertIs(address.person, person)

    def test_minimum_one2one(self):
        registry = self.init_registry(_minimum_one2one)
        self.assertTrue(hasattr(registry.Person, 'address'))
        self.assertTrue(hasattr(registry.Person, 'address_id'))
        address = registry.Address.insert()
        person = registry.Person.insert(
            name="Jean-sébastien SUZANNE", address=address)

        self.assertIs(address.person, person)

    def test_one2one_multi_entry_for_same(self):
        registry = self.init_registry(_minimum_one2one)
        address = registry.Address.insert()
        p1 = registry.Person.insert(
            name="Jean-sébastien SUZANNE", address=address)
        self.assertIs(p1.address, address)
        p2 = registry.Person.insert(name="Franck BRET", address=address)
        self.assertIs(p2.address, address)
        self.assertIsNone(p1.address_id)

    def test_one2one_with_str_model(self):
        registry = self.init_registry(_one2one_with_str_method)
        self.assertTrue(hasattr(registry.Person, 'address'))
        self.assertTrue(hasattr(registry.Person, 'address_id'))
        address = registry.Address.insert()
        person = registry.Person.insert(
            name="Jean-sébastien SUZANNE", address=address)
        self.assertIs(address.person, person)

    def test_minimum_one2one_without_backref(self):
        with self.assertRaises(FieldException):
            self.init_registry(_minimum_one2one_without_backref)

    def test_minimum_one2one_with_one2many(self):
        with self.assertRaises(FieldException):
            self.init_registry(_minimum_one2one_with_one2many)

    def test_complet_with_multi_foreign_key(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                @classmethod
                def define_table_args(cls):
                    table_args = super(Test2, cls).define_table_args()
                    return table_args + (ForeignKeyConstraint(
                        ['test_id', 'test_id2'], ['test.id', 'test.id2']),)

                id = Integer(primary_key=True)
                test_id = Integer(
                    foreign_key=(Model.Test, 'id'), nullable=False)
                test_id2 = String(
                    foreign_key=(Model.Test, 'id2'), nullable=False)
                test = One2One(model=Model.Test,
                               remote_columns=('id', 'id2'),
                               column_names=('test_id', 'test_id2'),
                               backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.test_id)
        self.assertEqual(test.id2, test2.test_id2)

    def test_complet_with_multi_foreign_key_without_constraint(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test_id = Integer(
                    foreign_key=(Model.Test, 'id'), nullable=False)
                test_id2 = String(
                    foreign_key=(Model.Test, 'id2'), nullable=False)
                test = One2One(model=Model.Test,
                               remote_columns=('id', 'id2'),
                               column_names=('test_id', 'test_id2'),
                               backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.test_id)
        self.assertEqual(test.id2, test2.test_id2)

    def test_with_multi_foreign_key_on_existing_column(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test_id = Integer(
                    foreign_key=(Model.Test, 'id'), nullable=False)
                test_id2 = String(
                    foreign_key=(Model.Test, 'id2'), nullable=False)
                test = One2One(model=Model.Test, backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.test_id)
        self.assertEqual(test.id2, test2.test_id2)

    def test_with_multi_foreign_key_on_existing_column2(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                other_test_id = Integer(
                    foreign_key=(Model.Test, 'id'), nullable=False)
                other_test_id2 = String(
                    foreign_key=(Model.Test, 'id2'), nullable=False)
                test = One2One(model=Model.Test, backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.other_test_id)
        self.assertEqual(test.id2, test2.other_test_id2)

    def test_with_multi_foreign_key_on_unexisting_column(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test = One2One(model=Model.Test, backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.test_id)
        self.assertEqual(test.id2, test2.test_id2)

    def test_with_multi_foreign_key_on_unexisting_named_column(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = String(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test = One2One(model=Model.Test,
                               column_names=('test_id', 'test_id2'),
                               backref="test2")

        registry = self.init_registry(add_in_registry)
        test = registry.Test.insert(id2="10")
        test2 = registry.Test2.insert(test=test)
        self.assertEqual(test.id, test2.test_id)
        self.assertEqual(test.id2, test2.test_id2)

    def test_with_multi_foreign_key_on_unexisting_named_column2(self):

        def add_in_registry():

            @register(Model)
            class Test:

                id = Integer(primary_key=True, unique=True)
                id2 = Integer(primary_key=True, unique=True)

            @register(Model)
            class Test2:

                id = Integer(primary_key=True)
                test = One2One(model=Model.Test, column_names=(
                    'other_test_id', 'other_test_id2'), backref="test2")

        with self.assertRaises(FieldException):
            self.init_registry(add_in_registry)
