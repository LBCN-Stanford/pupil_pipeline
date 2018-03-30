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
    # TODOOOO0
    pass


def save_params(params):
    with open(make_path('parameters', '.py', **params), 'w') as f:
        f.write('params = {}\n')
        for k, v in params.items():
            if type(v) == str:
                f.write("params['" + str(k) + "']" +
                        " = " + "'" + str(v) + "'" + '\n')
            else:
                f.write("params['" + str(k) + "']" + " = " + str(v) + '\n')
