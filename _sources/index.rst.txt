Mikufetch — cute cross-platform fetch tool with Miku ASCII 💙
===============================================================


Mikufetch is a tiny cross-platform fetch tool that shows system information
with Hatsune Miku ASCII art. Because why should nerd tools look boring? 😌

**Features**
- Runs on Windows, Linux, maybe macOS 👀
- Minimal dependencies
- ANSI color output
- JSON mode for scripts and automation

Example usage
-------------

.. code-block:: bash

    mikufetch
    mikufetch --no-art
    mikufetch --json

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Sections:

   usage
   modules

API Reference
=============

.. autosummary::
   :toctree: _autosummary
   :recursive:

   mikufetch
   mikufetch.cli
   mikufetch.info
   mikufetch.art
