# coding=u8
# Copyright 2014-2015 Secken, Inc.  All Rights Reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# NOTICE:  All information contained herein is, and remains
# the property of Secken, Inc. and its suppliers, if any.
# The intellectual and technical concepts contained
# herein are proprietary to Secken, Inc. and its suppliers
# and may be covered by China and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Secken, Inc..
#
# 注意：此处包含的所有信息，均属于Secken, Inc.及其供应商的私有财产。
# 此处包含的所有知识、专利均属于Secken, Inc.及其供应商，属于商业秘密，
# 并受到中国和其他国家的法律保护。这些信息及本声明，除非事先得到
# Secken, Inc.的书面授权，否则严禁复制或传播。
#
# @author     xupengjie (pengjiexu@secken.com)
# @version    1.0.0
#


#coding=u8

from setuptools import setup, find_packages
setup(
    name="secken-api",
    version="3.1.1",
    description="yangcong python sdk",
    author="Secken",
    url="http://www.secken.com",
    license="LGPL",
    packages=find_packages(),
    scripts=["secken.py"],
    py_modules=['secken']
)
