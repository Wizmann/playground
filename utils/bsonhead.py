#coding=utf-8
'''
get the head of a bson file

`pip install pymongo` before you use this script

feel free to contact me if there is any problems
'''

import bson
import argparse
import pprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', dest='num', type=int, default=5, help='number of bson items')
    parser.add_argument('--pprint', dest='pprint', action='store_true', default=False, help='prettified print')
    parser.add_argument('-o', '--output', dest='output_file', type=str, help='output bson file')
    parser.add_argument('input_file', type=str, help='input bson file')

    args = parser.parse_args()

    assert args.num > 0
    assert args.input_file

    if args.output_file:
        out_file = open(args.output_file, 'wb')
    else:
        out_file = None

    with open(args.input_file, 'rb') as in_file:
        for i, entry in enumerate(bson.decode_file_iter(in_file)):
            if i >= args.num:
                break

            if out_file is None:
                if args.pprint:
                    pprint.pprint(entry)
                else:
                    print entry
            else:
                out_file.write(bson.BSON.encode(entry))

    if out_file:
        out_file.close()

