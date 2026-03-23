from __future__ import annotations

import argparse
import json

from .services import analyze_change, generate_passport, list_changes, list_products, overview_metrics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ThreadPass PLM demo CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("products", help="List demo products")
    subparsers.add_parser("changes", help="List demo change requests")
    subparsers.add_parser("overview", help="Show overview metrics")

    passport_parser = subparsers.add_parser("passport", help="Generate passport JSON")
    passport_parser.add_argument("product_id", help="Product ID, such as PRD-100")

    impact_parser = subparsers.add_parser("impact", help="Analyze a change request")
    impact_parser.add_argument("change_id", help="Change ID, such as ECO-101")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "products":
        payload = list_products()
    elif args.command == "changes":
        payload = list_changes()
    elif args.command == "overview":
        payload = overview_metrics()
    elif args.command == "passport":
        payload = generate_passport(args.product_id)
    elif args.command == "impact":
        payload = analyze_change(args.change_id)
    else:
        parser.error("Unknown command")
        return

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
