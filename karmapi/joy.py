"""
Magic backend selector for pig.

Called joy because of Great Uncle Urban's letter, where joy looked like pig

"""

import os

BACKEND = 'qt'

if 'PIG' in os.environ:
    BACKEND = os.environ['PIG']

def set_backend(backend):

    global BACKEND

    BACKEND = backend
