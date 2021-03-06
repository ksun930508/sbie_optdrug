# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy 
from os.path import exists
from sbie_optdrug.result.tab_s3 import program
from pdb import set_trace


def check_outputs(config):

    exist_list = [exists(config['output'][key]) for key \
        in config['output'] ]

    return numpy.product(exist_list)


def test(with_small, force):
    
    config = program.getconfig()

    if not check_outputs(config) or force:
        program.run(config)

    assert check_outputs(config)

