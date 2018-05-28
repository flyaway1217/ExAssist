Gathering infomation
********************
``Assist`` is the only class in ExAssist framework.
This section provides basic usage of ``Assist``.

.. _create-assist:

Create an Assist
================

In order to use ExAssist to assist your experiment, you first need to instantiate an intance of ``Assist``:

.. code-block:: python

    import ExAssist as EA
    assist = EA.getAssist('Test')

When calling ``getAssist`` method, ExAssist will instantiate a new ``Assist`` instance if it does not exist.
The name ``Test`` is the unique identifier for the new ``Assist`` instance.
Just like `logging <https://docs.python.org/3.6/library/logging.html#logging.getLogger>`_ you can access the same instance anywhere in your source code:

.. code-block:: python

    assist = EA.getAssist('Test')

After getting an instance of ``Assist``, you need to setup some basic information:

    - The root path of your experiemnt records.(default: ``./Experiments/``)
    - The path of template directory, which contains the template files. Templates files are used to render data into html files.
    - The path of `Config <https://docs.python.org/3.6/library/configparser.html#configparser.ConfigParser>`_  file, which contains all the config information of your experiment.


A simple example is like this:

.. code-block:: python

    # Get the Assist instance
    assist = EA.getAssist('Test')
    # Set up the root path of experiment records
    assist.ex_dir = 'tests/Experiments/'
    # Set up the config
    assist.config_file = './config.ini'


Once setting up all the informaion, you can start your experiments.

Observe an Experiment
=====================

The first function of ExAssist is to observe en experiment automatically.
ExAssist uses context manager to observe your experiment::

    with EA.start(assist) as assist:
        # Your experiment happens here

When you entering this context, ExAssist will automatically:
    - Create a uniqe directory which will be used to save all the information about this experiment.
    - Gather meta information about your experiment, like your starting time and environment information.
    - Load the config file from the path you provided. You can access the `Config <https://docs.python.org/3.6/library/configparser.html#configparser.ConfigParser>`_ object by ``assist.config``.

.. NOTE::
    Once entering the context, you can not modify the basic information about ``Assist`` covered in last section, see :ref:`create-assist`.

When you finish running your experiment and leaving this context, ExAssist will automatically:
    - Record the status (success, failed or interrupted) of this experiment
    - Generate an html file that contains all the information of this experiment.

ExAssist collects lots of information about an experiment:

    - time it was started, time it stopped and cpu time it used.
    - the used configuration
    - status of this experiment
    - basic information about the machine it runs on
    - packages the experiment depends on and their versions
    - data added with ``assist.info``
    - data added with ``assist.result``

Directory Structure
-------------------

All the information (except the last two points) above is gathered and saved automatically, you don't need to write any code.
For each experiment running, ExAssist will create a new sub-directory in the path of ``ex_dir`` and stores several files in there:

.. code-block:: console

    Experiments/
    ├── 0
    │   ├── config.ini
    │   ├── index.html
    │   ├── info.json
    │   └── run.json
    ├── 1
    │   ├── config.ini
    │   ├── index.html
    │   ├── info.json
    │   └── run.json


As we can see above, ExAssist will also generate a report (``index.html``) for each run from given template files. See :doc:`/template`.

Assist an Experiment
====================

The second function of ExAssist is to assist your experiment.
It gives the abilities:

    - Access the configuration in any places. This can help you avoid passing a lot configurations through different files:

    .. code-block:: python

        import ExAssist as EA

        assist = EA.getAssist('Test')
        rate = assist.config.get('default','rate')

    - Record the running information without writing extra IO functions. ExAssis can help you save all the temporary information during the experiment, such as loss and gradients.

    .. code-block:: python

        import ExAssis as EA

        assist = EA.getAssist('Test')
        with EA.start(assist) as assist:
            # Here starts your experiments.
            for i in range(100):
                assist.info['loss'] = 100 - i
                assist.step()

    In the code above, we record ``loss`` value for each iteration. Method ``step()`` tells ExAssist that the current iteration is finished.
    ``assis.info`` is dictionary which means you can put anything you want into this variable.
    The ``info`` dictionary is meant to store temporary information about the experiment, like training loss for each epoch or the total number of parameters.
    It is updated once you invoke ``step`` method.
    You can add whatever information you like to ``info``.
    Code in the above will generate a list like this:

    .. code-block:: python

        [{'loss':100}, {'loss':99}, {'loss':98}, ...]

    Once you entering the context, you can access and update following variables:

    - ``assist.info``: You can use ``info`` to save any temporary value that you need to analysis, like traning loss.
    - ``assist.result``: ``result`` are designed to keep the evaluation results of this experiment. ``result`` does not affeced by ``step()`` method.
    - ``assist.run_path``: Read-only. You can access the path of current experiment data. This is useful when you want to save your model in the same directory with its meta information.
    - ``assist.epoch``: Read-only. Indicates the internal epoch number of ExAssist. It increases every time when you invoke ``step()`` method.
