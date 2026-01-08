import sys
import argparse
from release_sentinel.core import run_checks
from release_sentinel.logging import setup_logging

def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Release safety gate"
    )
    parser.add_argument(
        "--env",
        required=True,
        help="Target environment (dev/stage/prod)"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release version (vX.Y.Z)"
    )

    args = parser.parse_args()

    exit_code = run_checks(
        env=args.env,
        version=args.version
    )
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
