"""
This module contains the client used for communicating with the SQC validation
server.
"""
from pathlib import Path
from tempfile import mkstemp
import os
import json
from typing import Any
from time import sleep
from uuid import uuid4

import minio
from minio import S3Error

request_bucket = "requests"
result_bucket = "results"


class SQCException(Exception):
    """
    SQC exception type raised by :func:`~sqclib.client.SQCClient`.

    Args:
        msg (str): Error message.
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class SQCClient:
    """
    Client used for communication with the SQC server.

    Args:
        url (str): URL of the minio server
        access_key (str): Access key provided by SQC administrators.
        secret_key (str): Secret key provided by SQC administrators.
        secure (bool, optional): Use HTTPS for communication.
            `True` by default.

    Examples:
        >>> client = SQCClient(
                'https://sqc-minio.dyn.cloud.e-infra.cz',
                'access_key',
                'secret_key',
                secure=True,
            )
        >>> client.validate('./struct.mmcif')
        {'results': 'ok'}
    """

    def __init__(self, url: str, access_key: str, secret_key: str, secure=True) -> None:
        self._minio = minio.Minio(
            url,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

    def submit(self, path: str | Path) -> str:
        """
        Submit a `.mmcif`, `.cif`, `.ent` or `.pdb` file for validation
        asynchronously.
        Returns an ID of the submitted validation.

        Args:
            path (str, :obj:`Path`): A string or a Path object of the
                file to be submitted.

        Returns:
            A request id that can be used for getting results with the
            :func:`~sqclib.client.SQCClient.get_result` function.

        Examples:
            >>> validation_id = client.submit('./struct.mmcif')
            >>> client.get_result(validation_id, timeout_s=60)
            {'results': 'ok'}
        """
        request_id = str(uuid4())
        ftype = str(path).split(".")[-1]
        if ftype not in {"mmcif", "cif", "ent", "pdb"}:
            raise SQCException("The file type extension is not valid")

        if ftype == "cif":
            ftype = "mmcif"
        elif ftype == "ent":
            ftype = "pdb"

        try:
            self._minio.fput_object(
                request_bucket, request_id, str(path), metadata={"ftype": ftype}
            )

        except S3Error as err:
            raise SQCException("Error during requesting validation") from err

        return request_id

    def validate(
        self, path: str | Path, timeout_s: int | None = None
    ) -> dict[str, Any] | None:
        """
        Validate a `.mmcif`, '.cif', `.ent` or `.pdb` file. This function blocks
        until the submitted file is validated. If you want to validate more
        structures, consider using the :func:`~sqclib.client.SQCClient.submit`
        and :func:`~sqclib.client.SQCClient.get_result` functions.

        Args:
            path (str, :obj:`Path`): A string or a Path object of the
                file to be submitted.
            timeout_s (int, optional): Timeout for waiting in seconds. No
                timeout by default.

        Returns:
            A dictionary containing the validation results or :obj:`None` if the
            validation timed out.

        Examples:
            >>> client.validate('./struct.mmcif', timeout_s=60)
            {'results': 'ok'}
        """
        val_id = self.submit(path)
        return self.get_result(val_id, timeout_s)

    def get_result(
        self, request_id: str, timeout_s: int | None = None
    ) -> dict[str, Any] | None:
        """
        Get a validation result from a request ID.

        Args:
            request_id (str): A valid request ID returned from
                :func:`~sqclib.client.SQCClient.submit`
            timeout_s (int, optional): Timeout for waiting in seconds. No
                timeout by default.

        Returns:
            A dictionary containing the validation results or :obj:`None` if the
            validation timed out.

        Examples:
            >>> validation_id = client.submit('./struct.mmcif')
            >>> client.get_result(validation_id, timeout_s=60)
            {'results': 'ok'}
        """
        # TODO: add timeout
        request_name = f"{request_id}.json"
        delay_s = 1
        while True:
            try:
                obj = self._minio.stat_object(result_bucket, request_name)

                if err := obj.metadata.get("X-Amz-Meta-Sqc-Error"):
                    raise SQCException(err)

                break
            except S3Error as err:
                if err.code == "NoSuchKey":
                    sleep(delay_s)
                    continue
                else:
                    raise SQCException("Error during result polling") from err

        return self._get_result(request_name)

    def _get_result(self, result_name: str) -> dict[str, Any]:
        try:
            fd, path = mkstemp(prefix=result_name)
            self._minio.fget_object(result_bucket, result_name, path)

            try:
                with open(path, "r") as tmpf:
                    return json.load(tmpf)
            finally:
                os.close(fd)
                os.unlink(path)

        except S3Error as err:
            raise SQCException("Error during result acquisition") from err
