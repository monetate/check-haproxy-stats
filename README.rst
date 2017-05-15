===============================
check haproxy stats
===============================


Check HAProxy related statistics


Features
--------

* Check HAProxy HTTP 5xx counts for various backends


Example Usage
--------------

Checking `check-trk` backend for HTTP 5xx Code Ratio during an interval of 60 seconds::

    check-haproxy-stats-5xx --backend check-trk --warning-ratio 0.01 --critical-ratio 0.02 \
        --username someone --password someone \
        --interval 60

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

