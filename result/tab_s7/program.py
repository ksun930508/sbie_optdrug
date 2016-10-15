# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from ipdb import set_trace
import json,re
from boolean3 import Model 
from boolean3_addon import attractor
from termutil import progressbar
from os.path import dirname,join
from sbie_optdrug.result import tab_s3
from boolean3_addon import attr_cy

# """ requirements """
# inputfile_a = join(dirname(__file__), 'TABLE.SXX.INPUTDATA.CSV')

# """ results """
# outputfile_a = join(dirname(__file__), 'TABLE.SXX.OUTPUTDATA.CSV')

config = {
    'program': 'Table_S3',
    'parameters': {
        # 'k1': 1,
        # 'k2': 2
        },
    'input': {
        # 'a': inputfile_a
        },
    'output': {
        # 'a': outputfile_a
        }
    }

def getconfig():
    
    return config

# def run(config=None):

#     with open(config['output']['a'], 'w') as fobj:
#         fobj.write('hello')

def run(config=None):

    def pinning():
        return {'S_hTRET': False}

    def set_value( state, name, value, p ):
        pinned_list = pinning()
        if name in pinned_list:
            value = pinned_list[name]

        setattr( state, name, value )
        return value

    data = tab_s3.load()
    eq_list = data['equation'].values.tolist()    

    node_set = set() 
    for eq in eq_list: 
        text2 = eq.replace('and', ' ')    
        text2 = text2.replace('or', ' ')    
        text2 = text2.replace('not', ' ')    
        text2 = text2.replace('*=', ' ')
        nodes = set(text2.split(' '))
        node_set = node_set.union(nodes)    
    
    for el in ['', '0', '1', 'True', 'False']: 
        if el in node_set: 
            node_set.remove(el)
    
    datadict = {} 
    
    for node in node_set: 
        if node == '':
            continue 
        data = { 'type': 'normal', 'value': None }
        datadict[node] = data
    init_list = []
    
    for node in node_set:
        init_list.append('%s=Random' % node)
    
    alleq = init_list + eq_list
    model_string = "\n".join(init_list + eq_list)

    attr_cy.build(model_string)

    res = attr_cy.run(samples=100000, steps=50, debug=False)
    
    json.dump(res, open('output.json', 'w'), indent=4)

    # model = Model( text=model_string, mode='sync')
    # model.parser.RULE_SETVALUE = set_value
    # model.initialize()
    # res = attractor.find_attractors(model=model, sample_size=1000, steps=30)
    # outputfile = 'test_basin_result.json'
    # json.dump(res, open(outputfile, 'w'), indent=2)
