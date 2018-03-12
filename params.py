import importlib
from misc import make_path


def get_params(argv):
    if len(argv) == 1:
        p = importlib.import_module('parameters_default').params
    else:
        p = importlib.import_module(argv[1][:-3]).params
    check_valid(p)
    return p


# TODO do some checks to make sure the praeters are valid!
def check_valid(p):
    pass


def save_params(params):
    out_dir, base_name = params['out_dir'], params['base_name']
    with open(make_path('parameters', '.py', out_dir=out_dir, base_name=base_name, **params), 'w') as f:
        f.write('params = {}\n')
        for k, v in params.items():
            if type(v) == str:
                f.write("params['" + str(k) + "']" +
                        " = " + "'" + str(v) + "'" + '\n')
            else:
                f.write("params['" + str(k) + "']" + " = " + str(v) + '\n')
