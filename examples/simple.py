import os
import sqclib

access_key = os.environ.get("SQC_ACCESS_KEY")
secret_key = os.environ.get("SQC_SECRET_KEY")

sqc = sqclib.SQCClient(
    "sqc-minio.dyn.cloud.e-infra.cz",
    access_key=access_key,
    secret_key=secret_key,
)

try:
    res = sqc.validate("test.mmcif")
    print(res)

except sqclib.SQCException:
    print("Something went awry")
    raise
