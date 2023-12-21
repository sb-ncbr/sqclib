from pathlib import Path
from tempfile import mktemp
import json
from typing import Any
from time import sleep
from uuid import uuid4

import minio
from minio import S3Error

request_bucket = 'requests'
result_bucket = 'results'

class SQCException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Request:
    def __init__(self, minio: minio.Minio, id: str):
        self._minio = minio
        self._id = id

    def wait_result(self, delay: int = 5) -> dict[str, Any]:
        while True:
            try:
                obj = self._minio.stat_object(
                    result_bucket,
                    self._id
                )

                if 'sqc-error' in obj.metadata:
                    raise SQCException(obj.metadata['sqc-message'])

                break
            except S3Error as err:
                if err.code == "NoSuchKey":
                    sleep(delay)
                    continue
                else:
                    raise SQCException("Error during result polling") from err

        return self._get_result()

    def _get_result(self) -> dict[str, Any]:
        try:
            path = mktemp(prefix=self._id)
            self._minio.fget_object(
                result_bucket,
                self._id,
                path
            )

            with open(path, 'r') as tmpf:
                return json.load(tmpf)

        except S3Error as err:
            raise SQCException("Error during result acquisition") from err


class SQCClient:
    def __init__(self, url: str, access_key: str, secret_key: str) -> None:
        self._minio = minio.Minio(
            url,
            access_key=access_key,
            secret_key=secret_key
        )

    def submit(self, path: str | Path) -> Request:
        id = str(uuid4())

        return Request(self._minio, id)
