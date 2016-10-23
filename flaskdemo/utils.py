from distutils.util import strtobool
import sys

#
# prompt() copied or adapted from http://mattoc.com/python-yes-no-prompt-cli.html
#
def prompt(query):
    """
        Prompt with a question on console, validate y/n response and return boolean result.
        Repeat until a valid value is entered.
    """ 
    sys.stdout.write('%s [y/n]: ' % query)
    val = input()
    try:
        ret = strtobool(val)
    except ValueError:
        sys.stdout.write('Please answer with a y/n\n')
        return prompt(query)
    return ret
