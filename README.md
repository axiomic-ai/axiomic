![Beta](https://img.shields.io/badge/status-beta-yellow)
[![Documentation Status](https://readthedocs.com/projects/axiomic-axiomic/badge/?version=latest&token=e91312bf81a79fe94d84cdf43f3eaf7ec7e55d9d51fb1a82ee0d24f73c5ec143)](https://axiomic-axiomic.readthedocs-hosted.com/en/latest/?badge=latest)


# Axiomic

Create Generative AI Apps and Agents which work. Join the beta today. You can see the [launch post](https://medium.com/@bitfort/06c6923fbf3c) for a detailed explanation.

In brief, Axiomic focuses on a few key tools that are necessary to make an agent. Axiomic works best combined with parts of the larger ecosystem, such as model providers (OpenAI, Anthropic, Together, etc.), vector databases, document extracts (e.g. LlamaIndex), and others.

Here, we focus on sipmle, reliable, portable, and introspectable tools and building blocks. What this specifically means:

- Easy to look under the hood to know what your agent is doing
- Easy to move between models
- Easy to get started

## Getting Started

Install the package:

    pip install axiomic

Pick your providers:

    # Choose at least one
    export TOGETHER_API_KEY=...
    export ANTHROPIC_API_KEY=sk-...
    export OPENAI_API_KEY=sk-...

Run inference:

    import axiomic as ax
    ax.infer('What has keys but cannot open locks?').print()

### Learn more

After getting started, 

* Review the [Tutorials](examples/tutorials/README.md)
* Read the [documentation](https://axiomic-axiomic.readthedocs-hosted.com/en/latest/index.html)
* Join the [discord](https://discord.gg/7MfjnuY8)


## Roadmap

Axiomic is still in beta and going through active development. Some upocming work includes;

- Streaming responses
- Agnet portability: save your agent to a file and share it
- Expanded retry systems for APIs and model errors
- Improved agent evaluation and quality tracking
- Additional demos and tutorials

Please share your thoughts here on github, or in the [discord](https://discord.gg/7MfjnuY8), on what you want to see next.
