import os
import sys
import argparse
from credentials import credentials

"""
this is a script which will allow the user to update, create, and query canvas courses based on the contents of either local repositories or remote github repositories.
"""



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance', type=str, help='specify canvas instance "c" consumer, "m" moringa, "a" academy xi, "e" enterprise, "v" vanguard')
    parser.add_argument('-s', "--saturncloud", action='store_true')
    
    
    args = parser.parse_args()
    
    API_KEY, API_PATH = credentials(args.instance)
    
    print(API_KEY,API_PATH, args.instance)