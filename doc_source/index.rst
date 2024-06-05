.. AIWeave documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Axiomic
===================================


.. note::

   Axiomic is in beta. Except things to constantly improve - and not stay the same.
   Join the conversation on github and discord to share your feedback.


Create AI Agents, work with generative models, easily.


Get get started,

.. code-block:: shell

   pip install axiomic 


Connect to your favorite generative model,

.. code-block:: shell

   # Choose at least one
   export TOGETHER_API_KEY=...
   export ANTHROPIC_API_KEY=sk-...
   export OPENAI_API_KEY=sk-...


Start generating,

.. code-block:: python

   import axiomic as ax

   ax.infer('What has keys but cannot open locks?').print()


After you get startd, the `github <https://github.com/ai-weave/weave>`_ has `tutorials <https://github.com/ai-weave/weave>`_ and `example applications <https://github.com/ai-weave/weave>`_.



.. toctree::
   :maxdepth: 2
   :caption: Learn More

   primitives
   models
   functions
   modules
   uagents
   data
   errors
