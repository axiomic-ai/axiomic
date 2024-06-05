
.. _quickstart:

Quickstart
===================



Setup and Install
-------------------


Install the package.


.. code-block:: bash

    python setup.py develop


Add your API variable to your environment.


.. code-block:: bash

    # Need at least ONE of the following
    export OPENAI_API_KEY=sk-...
    export ANTHROPIC_API_KEY=sk-...


Basic Example Usage
-------------------

.. code-block:: python

    import weave
    weave.infer('What is the meaning of life?').print()


Choosing your LLM
-------------------

.. code-block:: python

    import weave
    import weave.configure.quick as qc

    with qc.BigLLM & qc.MaxTokens256 & qc.Temperature0_5:
        weave.infer('What is the meaning of life?').print()




Next Steps
-------------------

TODO
