ExAssist
========

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
