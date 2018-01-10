ExAssist
========

|build-status| |docs|

``ExAssist`` is an light-weight assist tool that can save your time from doing experiments.
It is designed to help you with:

    1. Track the configurations for each experiment.
    2. Record any temporary data during  experiments.
    3. Gather host information for each experiment.

Installation
============

.. code:: python
    
    pip install ExAssist

Example
=======

.. code:: python
    
    import ExAssist as EA

    # Get an instance of ExAssist just like getting a logger.
    assist = EA.getAssist('Test')
    with EA.start(assist) as assist:
        # Here starts your experiments.
        for i in range(100):
            assist.info['loss'] = 100 - i
            assist.step()

Documents
=========

`<http://exassist.zhouyichu.com/en/latest/>`_

 .. |docs| image:: https://readthedocs.org/projects/exassist/badge/?version=latest
    :target: http://exassist.readthedocs.io/en/latest/?badge=latest
    :scale: 100%
    :alt: Documentation Status

.. |build-status| image:: https://travis-ci.org/flyaway1217/ExAssist.svg?branch=master
    :target: https://travis-ci.org/flyaway1217/ExAssist
