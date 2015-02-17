# -*- coding: utf-8 -*-
import sys
import os
import logging
import random

import re
import imp
import inspect

IMPORTED_MODULE = 'rules1'
import rules1 as rules

class Rules(object):
    def __init__(self):
        ''' 
        ''' 
        self.log = logging.getLogger('Rules')
        #self.log.debug('__init__ start')
        
        #self.log.debug('__init__ end')
        return None
    
    def setup(self):
        ''' 
        ''' 
        #self.log.debug('setup start')
        rules_list = list()
        fp, pathname, description = imp.find_module(IMPORTED_MODULE, None)
        
        #try:
            #rules = imp.load_module(IMPORTED_MODULE, fp, pathname, description )
        #finally:
            #if fp:
                #fp.close()
        
        m_list = dir(rules)
        
        for m in m_list:
            if m[:4] == 'Rule':
                s = 'rules.%s()' % m
                rules_list.append(eval(s))
        rules_list = sorted(rules_list, key=lambda rule: rule.rank)
        #members = inspect.getmembers(rules)
        #for m in members:
            #if m[1][:6] == '<class':
                #print m[1]
            #if inspect.isclass(m[0]):
                #print 'class****', m
            #else:
                #print m
        #self.log.debug('setup end')
        return rules_list
    
    