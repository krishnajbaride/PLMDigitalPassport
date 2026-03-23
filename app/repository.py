from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .schemas import BomEdge, ChangeRequest, Part, Product

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class DataStore:
    def __init__(self) -> None:
        self.products = self._load_products()
        self.parts = self._load_parts()
        self.bom_edges = self._load_bom_edges()
        self.change_requests = self._load_changes()

        self.children_map: dict[str, list[BomEdge]] = {}
        self.parent_map: dict[str, list[BomEdge]] = {}
        for edge in self.bom_edges:
            self.children_map.setdefault(edge.parent_id, []).append(edge)
            self.parent_map.setdefault(edge.child_id, []).append(edge)

    def _load_products(self) -> dict[str, Product]:
        data = json.loads((DATA_DIR / "products.json").read_text())
        return {item["id"]: Product(**item) for item in data}

    def _load_parts(self) -> dict[str, Part]:
        data = json.loads((DATA_DIR / "parts.json").read_text())
        return {item["id"]: Part(**item) for item in data}

    def _load_bom_edges(self) -> list[BomEdge]:
        data = json.loads((DATA_DIR / "boms.json").read_text())
        return [BomEdge(**item) for item in data]

    def _load_changes(self) -> dict[str, ChangeRequest]:
        data = json.loads((DATA_DIR / "changes.json").read_text())
        return {item["id"]: ChangeRequest(**item) for item in data}

    def get_product(self, product_id: str) -> Product | None:
        return self.products.get(product_id)

    def get_part(self, part_id: str) -> Part | None:
        return self.parts.get(part_id)

    def get_node_name(self, node_id: str) -> str:
        if node_id in self.products:
            return self.products[node_id].name
        if node_id in self.parts:
            return self.parts[node_id].name
        return node_id


@lru_cache(maxsize=1)
def get_store() -> DataStore:
    return DataStore()
