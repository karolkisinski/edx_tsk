import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Currency conversion script")
    parser.add_argument("-m", "--mode", choices=["dev", "prod"], default="dev",
                        help="Choose operating mode (dev or prod)")
    parser.add_argument("-c", "--currency", help="Specify currency")
    parser.add_argument("-a", "--amount", help="Specify amount")
    return parser.parse_args()
