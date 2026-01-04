import sys, argparse, logging
from deploy_guard.logging import setup_logging
from deploy_guard.core.env_gate import validate_env
from deploy_guard.core.health_checks import check_disk, check_memory
from deploy_guard.core.deploy_k8s import deploy, rollback
from deploy_guard.core.api_checks import get_with_retry
from deploy_guard.core.pipeline import run_pipeline
from deploy_guard.core.notes.release_notes import generate_notes
from deploy_guard.core.release_guard import create_tag


def main():
    setup_logging()
    parser = argparse.ArgumentParser(prog="deploy-guard")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("env")
    sub.add_parser("disk")
    sub.add_parser("memory")

    apply = sub.add_parser("apply")
    apply.add_argument("--manifest", required=True)

    rb = sub.add_parser("rollback")
    rb.add_argument("--deployment", required=True)
    rb.add_argument("--namespace", default="default")

    api = sub.add_parser("api")
    api.add_argument("--url", required=True)

    pipe = sub.add_parser("pipeline")
    pipe.add_argument("--manifest", required=True)
    pipe.add_argument("--url", required=True)

    notes = sub.add_parser("notes")
    notes.add_argument("-n", type=int, default=10)

    tag = sub.add_parser("tag")
    tag.add_argument("--version", required=True)

    args = parser.parse_args()
    try:
        if args.cmd == "env":
            sys.exit(validate_env())
        elif args.cmd == "disk":
            sys.exit(check_disk())
        elif args.cmd == "memory":
            sys.exit(check_memory())
        elif args.cmd == "apply":
            sys.exit(deploy(args.manifest))
        elif args.cmd == "rollback":
            sys.exit(rollback(args.deployment, args.namespace))
        elif args.cmd == "api":
            sys.exit(get_with_retry(args.url))
        elif args.cmd == "pipeline":
            sys.exit(run_pipeline(args.manifest, args.url))
        elif args.cmd == "notes":
            sys.exit(generate_notes(args.n))
        elif args.cmd == "tag":
            sys.exit(create_tag(args.version))
    except Exception as e:
        logging.getLogger("deploy_guard").error("ERROR: %s", e)
        sys.exit(2)
