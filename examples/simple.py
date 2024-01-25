import sqclib

sqc = sqclib.SQCClient(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin"
)

try:
    req = sqc.submit('test.mmcif')
    res = req.wait_result()
    print(res)

except sqclib.SQCException:
    print("Something went awry")
    raise

