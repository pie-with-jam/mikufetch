"""Entry point for Mikufetch as a standalone script.

Imports the CLI main function and runs it, exiting with its return code.
"""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
