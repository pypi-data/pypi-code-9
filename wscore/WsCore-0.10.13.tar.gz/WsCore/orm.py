#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Waner <wanernet@qq.com>'
__all__ = ["Field", "Model", "ModelMetaclass", "StringField", "BooleanField",
           "IntegerField", "BigIntegerField", "FloatField", "TextField",
           "TimestampField"]

import sys
from WsCore.db.MySQLHelper import MySQLHelper
from WsCore.kenel.JSON import JSON

reload(sys)
sys.setdefaultencoding('utf8')


class Field(object):
    def __init__(self, name, column_type, primary_key=False, default_value=None):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default_value = default_value

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default_value=None, column_type='varchar(50)'):
        super(StringField, self).__init__(name, column_type, primary_key, default_value)


class BooleanField(Field):
    def __init__(self, name=None, default_value=False):
        super(BooleanField, self).__init__(name, 'boolean', False, default_value)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0):
        super(IntegerField, self).__init__(name, 'int', primary_key, default_value)


class BigIntegerField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0):
        super(BigIntegerField, self).__init__(name, 'bigint', primary_key, default_value)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0.0):
        super(FloatField, self).__init__(name, 'real', primary_key, default_value)


class TextField(Field):
    def __init__(self, name=None, default_value=None):
        super(TextField, self).__init__(name, 'text', False, default_value)


class TimestampField(Field):
    def __init__(self, name=None, default_value=None):
        super(TimestampField, self).__init__(name, 'timestamp', False, default_value)


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        # print ('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = attrs.get('__primary_key__', None) or None
        for k, v in attrs.items():
            # from Field import Field

            if isinstance(v, Field):
                # print ('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if primary_key:
                    fields.append(k)
                else:
                    if v.primary_key:
                        # if primary_key:
                        # raise StandardError('Duplicate primary key for field: %s' % k)
                        primary_key = k
                    else:
                        fields.append(k)
        if not primary_key:
            raise StandardError('Primary key not found.')
        for key in mappings.keys():
            attrs.pop(key)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        # assert isinstance(table_name, object)
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        return type.__new__(mcs, name, bases, attrs)


class Model(dict):
    """ 实体继承基类
    """
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                setattr(self, key, value)
        return value

    def insert(self):
        """ 实体数据插入数据库，注意：插入字段根据实体已赋值字段生成
        :return: 返回新增主键值
        """
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            if v.name != self.__primary_key__:
                val = self.getValue(v.name)
                if val is not None:
                    fields.append(v.name)
                    params.append('?')
                    args.append(val)

        sql_str = 'INSERT INTO %s (%s) VALUES (%s);' % (self.__table__, ','.join(fields), ','.join(params))
        sql_str = sql_str.replace('?', '%s')
        args = tuple(args)
        with MySQLHelper(self.__conn__) as sql:
            return sql.insert(sql_str, args)

    def save(self):
        """ 根据主键值 更新实体数据
        :return: 返回影响行数
        """
        fields = []
        args = []
        for k, v in self.__mappings__.iteritems():
            if v.name != self.__primary_key__:
                val = self.getValue(v.name)
                if val is not None:
                    fields.append(v.name)
                    args.append(val)

        sql_str = 'UPDATE `%s` SET %s WHERE `%s`=?;' % (self.__table__,
                                                        ', '.join(map(
                                                            lambda f: '`%s`=?' % (self.__mappings__.get(f).name or f),
                                                            fields)),
                                                        self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        args.append(self.getValueOrDefault(self.__primary_key__))
        args = tuple(args)

        with MySQLHelper(self.__conn__) as sql:
            return sql.execute(sql_str, args)

    def remove(self):
        """ 根据主键 删除记录
        :return: 返回受影响的行数
        """
        args = tuple([self.getValue(self.__primary_key__)])
        sql_str = 'DELETE FROM `%s` WHERE `%s`=?' % (self.__table__, self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        with MySQLHelper(self.__conn__) as sql:
            return sql.execute(sql_str, args)

    def hidden(self):
        """ 根据主键 屏蔽记录
        :return: 返回受影响的行数
        """
        args = tuple([self.getValue(self.__primary_key__)])
        sql_str = 'UPDATE `%s` SET is_invalid=1 WHERE `%s`=?' % (self.__table__, self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        with MySQLHelper(self.__conn__) as sql:
            return sql.execute(sql_str, args)

    @classmethod
    def execute(cls, sql_str, where=None, args=None):
        """ 执行SQL语句
        :param sql_str: delete from %s 或者 update %s set
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return: 返回受影响的行数
        """
        sql_str = sql_str % cls.__table__
        if where:
            sql_str += ' where %s' % where

        sql_str = sql_str.replace('?', '%s')
        with MySQLHelper(cls.__conn__) as sql:
            return sql.execute(sql_str, args)

    @classmethod
    def is_exists(cls, where=None, args=None):
        """
        判断记录是否存在
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return:返回布尔值
        """
        sql_str = "select 1 from %s"
        result = cls.execute(sql_str, where, args)
        # print "is_exists: %s" % result
        return True if result == 1 else False

    @classmethod
    def get_sql_str(cls, top=0, field=None, where=None):
        """ 生成查询字符串
        :param top: top数量，如：10
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :return:
        """
        sql_str = 'select `%s`,%s from %s%s' % (cls.__primary_key__, ', '.join(cls.__fields__),
                                                cls.__table__, ('' if top == 0 else (' limit %s ' % top)))
        if field:
            sql_str = 'select %s from %s%s' % (field, cls.__table__, ('' if top == 0 else (' limit %s ' % top)))

        if where:
            sql_str += ' where %s' % where
        # print sql_str
        return sql_str.replace('?', '%s')

    @classmethod
    def query(cls, top=0, field=None, where=None, args=None):
        """ 多条件查询结果集
        :param top: top数量，如：10
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return: 返回实体记录集对象 或 None
        """
        sql_str = cls.get_sql_str(top, field, where)
        with MySQLHelper(cls.__conn__) as sql:
            rs = sql.query(sql_str, args)
            return [cls(**r) for r in rs] if rs else None

    @classmethod
    def first(cls, field=None, where=None, args=None):
        """ 多条件查找唯一记录
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return:返回单一记录实体对象 或 None
        """
        sql_str = cls.get_sql_str(0, field, where)
        with MySQLHelper(cls.__conn__) as sql:
            r = sql.first(sql_str, args)
            return cls(**r) if r else None

    @classmethod
    def first_pk(cls, pk, field=None):
        """ 根据主键查找唯一记录
        :param pk: 主键值，如：5
        :param field: 读取字段，如：id,account,pwd
        :return:返回单一记录实体对象 或 None
        """
        sql_str = cls.get_sql_str(field=field, where=cls.__primary_key__ + '=?')
        # print sql_str
        with MySQLHelper(cls.__conn__) as sql:
            r = sql.first(sql_str, pk)
            return cls(**r) if r else None

    @classmethod
    def limit(cls, current=0, page_size=0, field=None, where=None, args=None):
        sql_str = 'select `%s`,%s from %s' % (cls.__primary_key__, ', '.join(cls.__fields__), cls.__table__)
        if field:
            sql_str = 'select %s from %s' % (field, cls.__table__)

        if current > 1:
            sql_str += ' where %s>=%s' % (cls.__primary_key__, current * page_size)
            if where:
                sql_str += ' and %s' % where
        else:
            if where:
                sql_str += ' where %s' % where

        sql_str += ' limit %s;SELECT FOUND_ROWS;' % page_size
        sql_str = sql_str.replace('?', '%s')
        with MySQLHelper(cls.__conn__) as sql:
            return sql.query(sql_str, args)

    def toJSON(self):
        """ 转换JSON格式
        :return:
        """
        return JSON.toJSON(self)

    @classmethod
    def fromJSON(cls, s):
        r = JSON.formJSON(s)
        return cls(**r) if r else None

        # def toXML(self):
        # json = self.toJSON()
        # return XML.toXML(json)
        #
        # @classmethod
        # def formXML(cls, xml):
        # json = JSON.toJSON(XML.formXML(xml), indent=4)
        # return cls.fromJSON(json)