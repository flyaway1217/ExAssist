Template
********

ExAssist uses `mako <http://www.makotemplates.org/>`_ to render html files.
Before running experiemnts, you need to specify the directory of template files.
The default directory of template is ``./templates``.
The default templates can be download :download:`here <./templates.zip>`.

Modify templates
================

In the templates,  there are two central files: ``index.html`` and ``ex.html``.

    - ``index.html`` is the template for index page, which lists the overall information of all the experiments you have done.
    - ``ex.html`` is the template for each run, which shows the detailed information of a specific experiment.

``index.html`` is rendered by `mako <http://www.makotemplates.org/>`_ like this:

.. code-block:: python

    path = os.path.join(template_path, 'index.html')
    tp = Template(filename=path)
    # records is a list of basic information of all experiments.
    s = tp.render(records=records)

Each item in ``records`` is a list of following information:

.. code-block:: python

            experiment_name
            start_time
            stop_time
            lapse_time
            cpu_time
            status
            comments
            result
 
    

``ex.html`` is rendered by `mako <http://www.makotemplates.org/>`_ like this:

.. code-block:: python

    path = os.path.join(template_path, 'ex.html')
    tp = Template(filename=path)
    # con is the config object, result is the data store in info.
    s = tp.render(config=con, result=result)


