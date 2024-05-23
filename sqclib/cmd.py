import argparse as ap
import json
import os
import sys
from sys import stderr

import sqclib


def sqc_submit(sqc_url: str, path: str, insecure: bool, timeout: float) -> None:
    access_key = os.environ.get("SQC_ACCESS_KEY")
    if not access_key:
        print("The SQC_ACCESS_KEY environment variable is undefined", file=stderr)
        sys.exit(1)

    secret_key = os.environ.get("SQC_SECRET_KEY")
    if not secret_key:
        print("The SQC_SECRET_KEY environment variable is undefined", file=stderr)
        sys.exit(1)

    sqc = sqclib.SQCClient(
        access_key, secret_key, url=sqc_url, secure=not insecure
    )

    res = sqc.validate(path, timeout)
    if res is None:
        print("Validation timed out", file=stderr)
        sys.exit(1)

    print(json.dumps(res))


def valid_timeout(value: str) -> float:
    timeout = float(value)
    if timeout < 0:
        raise ap.ArgumentTypeError("The timeout must be a non-negative number")
    return timeout


def main_cli():
    parser = ap.ArgumentParser()
    parser.add_argument("path", help="Path to the MMCIF/PDB/ENT file to submit to SQC.")
    parser.add_argument("-u", "--url", default="sqc-minio.dyn.cloud.e-infra.cz")
    parser.add_argument(
        "-k",
        "--insecure",
        default=False,
        action="store_const",
        const=True,
        help="Allow insecure connection.",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=120,
        help="Timeout for the validation in seconds. Two minutes by default. Zero signifies no timeout",
        action="store",
        type=float,
    )

    args = parser.parse_args()

    sqc_submit(args.url, args.path, args.insecure, args.timeout)
    sys.exit(0)
