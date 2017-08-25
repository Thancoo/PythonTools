#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pdb
import logging
logging.basicConfig(level=logging.INFO)
from sys import path
path.append('../')
path.append('../../')
import Decorator.CommonDecorator
from Entitys.Store import Store
from Entitys.User import User


def UserTest():
    user = User()
    pdb.set_trace()
    user.find()


def StoreTest():
    stor = Store()
    pdb.set_trace()
    res = stor.find()


@Decorator.CommonDecorator.Injector('ConfigerManager.ConstConfig')
class test1():

    def testmethod1(self):
        pdb.set_trace()
        pass


def main():
    ii = test1()
    ii.testmethod1()

if __name__ == '__main__':
    main()
