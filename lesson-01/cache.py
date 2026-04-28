from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class _Node:
    key: str
    value: str
    prev: Optional["_Node"] = None
    next: Optional["_Node"] = None


class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = max(0, int(capacity))
        self._items: dict[str, _Node] = {}

        self._head = _Node(key="__HEAD__", value="")
        self._tail = _Node(key="__TAIL__", value="")
        self._head.next = self._tail
        self._tail.prev = self._head

    def _unlink(self, node: _Node) -> None:
        prev = node.prev
        nxt = node.next
        if prev is not None:
            prev.next = nxt
        if nxt is not None:
            nxt.prev = prev
        node.prev = None
        node.next = None

    def _insert_after_head(self, node: _Node) -> None:
        first = self._head.next
        node.prev = self._head
        node.next = first
        self._head.next = node
        if first is not None:
            first.prev = node

    def _touch(self, node: _Node) -> None:
        self._unlink(node)
        self._insert_after_head(node)

    def _evict_if_needed(self) -> None:
        while len(self._items) > self.capacity:
            lru = self._tail.prev
            if lru is None or lru is self._head:
                return
            self._unlink(lru)
            self._items.pop(lru.key, None)

    def get(self, key: str) -> str:
        node = self._items.get(key)
        if node is None:
            return ""
        self._touch(node)
        return node.value

    def set(self, key: str, value: str) -> None:
        if self.capacity <= 0:
            self._items.clear()
            self._head.next = self._tail
            self._tail.prev = self._head
            return

        node = self._items.get(key)
        if node is not None:
            node.value = value
            self._touch(node)
            return

        node = _Node(key=key, value=value)
        self._items[key] = node
        self._insert_after_head(node)
        self._evict_if_needed()

    def rem(self, key: str) -> None:
        node = self._items.pop(key, None)
        if node is None:
            return
        self._unlink(node)
