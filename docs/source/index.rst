Welcome to sqclib's documentation!
==================================

Command line utility
--------------------
In addition to the python API, the library also provides a command line utility
``sqc``. It can be used to quickly submit a single request to the SQC server and
get a JSON response. To use the client, the environment variables
``SQC_ACCESS_KEY`` and ``SQC_SECRET_KEY`` must be set with your credentials.
.. code-block::

   $ sqc submit structure.mmcif
   $ sqc submit structure.pdb

Python library API
----------
.. automodule:: sqclib.client
   :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
