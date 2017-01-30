"""
The joyful pig
"""
import joy

import argparse
import curio

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', default='tk')


def main():

    args = get_parser.parse_args()

    # set the backend
    joy.set_backend(args.pig)

    # import pig after setting joy backend
    from karmapi import pig, piglet

    meta = [
        dict(name="MagicCarpet"),
        dict(name="karmapi.widgets.InfinitySlalom"),
        dict(name="Mclock")]
            
        

    app = pig.buils_joy((meta)

    pig.run(app)
    
