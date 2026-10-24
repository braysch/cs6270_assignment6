import argparse

parser = argparse.ArgumentParser(description="My program")
parser.add_argument("--arg1", required=True, help="...")
parser.add_argument("--arg2", required=True, help="...")
parser.add_argument("--arg3", required=True, help="...")
parser.add_argument("--arg4", required=True, help="...")
args = parser.parse_args()

print(args)