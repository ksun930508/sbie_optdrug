from os.path import exists
from sbie_optdrug.result.tab_s3 import program


def test(with_small, force):
    
    config = program.getconfig()

    if not exists(config['output']) or force:
        program.run(config)

        assert exists(config['output'])