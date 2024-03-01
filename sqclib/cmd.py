import argparse as ap
import os
from sys import stderr

import sqclib


def sqc_submit(sqc_url: str, path: str) -> None:
    access_key = os.environ.get("SQC_ACCESS_KEY")
    if not access_key:
        print("The SQC_ACCESS_KEY environment variable is undefined", file=stderr)
        exit(1)

    secret_key = os.environ.get("SQC_SECRET_KEY")
    if not secret_key:
        print("The SQC_SECRET_KEY environment variable is undefined", file=stderr)
        exit(1)

    sqc = sqclib.SQCClient(
        sqc_url, access_key=access_key, secret_key=secret_key, secure=False
    )

    res = sqc.validate(path)
    print(res)


def main_cli():
    parser = ap.ArgumentParser()
    parser.add_argument("path", help="path to the MMCIF/PDB/ENT file to submit to SQC")
    parser.add_argument("-u", "--url", default="https://sqc-minio.dyn.cloud.e-infra.cz")

    args = parser.parse_args()

    sqc_submit(args.url, args.path)
