![Beta](https://img.shields.io/badge/status-beta-yellow)
[![Documentation Status](https://readthedocs.com/projects/axiomic-axiomic/badge/?version=latest&token=e91312bf81a79fe94d84cdf43f3eaf7ec7e55d9d51fb1a82ee0d24f73c5ec143)](https://axiomic-axiomic.readthedocs-hosted.com/en/latest/?badge=latest)


# Axiomic

Create Generative AI Apps which work. Join the beta today.

Learn more by reading the [launch post](examples/tutorials/README.md) and Together AI's blog post.

## Getting Started

Install the package:

    pip install axiomic

Pick your providers:

    # Choose at least one
    export TOGETHER_API_KEY=...
    export ANTHROPIC_API_KEY=sk-...
    export OPENAI_API_KEY=sk-...
    Start generating,

Run inference:

    import axiomic as ax
    ax.infer('What has keys but cannot open locks?').print()

### Learn more

After getting started, 

* Review the [Tutorials](examples/tutorials/README.md)
* Read the [documentation](https://axiomic-axiomic.readthedocs-hosted.com/en/latest/index.html)
* Join the [discord](https://discord.gg/7MfjnuY8)

