
.. _models:

Models
===================


Choosing LLMs and parameters are done through `with` contexts.

.. code-block:: python

    import axiomic as ax

    with ax.Generic.Text.Large & ax.models.MaxTokens256 & ax.models.Temperature0_5:
        ax.infer('What is the meaning of life?').print()


Configuration
-------------------

.. automodule:: axiomic.models
   :members:
   :undoc-members:
   :show-inheritance:


OpenAI
-------------------

.. autoclass:: axiomic.models.OpenAI
   :members:
   :undoc-members:
   :show-inheritance:


Anthropic
-------------------

.. autoclass:: axiomic.models.Anthropic
   :members:
   :undoc-members:
   :show-inheritance:

Together AI
-------------------

.. autoclass:: axiomic.models.Together
   :members:
   :undoc-members:
   :show-inheritance:

