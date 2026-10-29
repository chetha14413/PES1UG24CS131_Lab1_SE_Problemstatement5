"""Manage a simple food-delivery order queue."""

import json
import math
from datetime import datetime
from pathlib import Path

DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}
VALID_STATUSES = {"placed", "cooking", "out_for_delivery", "delivered"}
orders = {}
id_counter = {"next": 1}
menu = DEFAULT_MENU.copy()


def create_order(customer, items, order_history=None):
    """Create an order after validating the customer and menu items."""
    if not isinstance(customer, str) or not customer.strip():
        raise ValueError("Customer name must not be empty.")
    if not isinstance(items, (list, tuple)) or not items:
        raise ValueError("An order must contain at least one item.")
    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError("Order items must be non-empty menu item names.")
    if order_history is not None and not isinstance(order_history, list):
        raise TypeError("Order history must be a list when provided.")

    unknown_items = [item for item in items if item not in menu]
    if unknown_items:
        raise ValueError(f"Unknown menu items: {', '.join(unknown_items)}")

    order_id = id_counter["next"]
    orders[order_id] = {
        "customer": customer.strip(),
        "items": list(items),
        "total": sum(menu[item] for item in items),
        "status": "placed",
    }
    if order_history is not None:
        order_history.append(order_id)
    id_counter["next"] += 1
    return order_id


def update_order_status(order_id, status):
    """Update an existing order with a recognized delivery status."""
    if not isinstance(order_id, int) or isinstance(order_id, bool):
        raise ValueError("Order ID must be an integer.")
    if order_id not in orders:
        raise KeyError(f"Order {order_id} does not exist.")
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    orders[order_id]["status"] = status


def read_menu_config(file="menu.json"):
    """Load a JSON menu, falling back only when the file is unavailable."""
    try:
        with Path(file).open("r", encoding="utf-8") as config_file:
            loaded_menu = json.load(config_file)
    except FileNotFoundError:
        menu.clear()
        menu.update(DEFAULT_MENU)
        return
    except json.JSONDecodeError as exc:
        message = f"Menu configuration is not valid JSON: {file}"
        raise ValueError(message) from exc

    if not isinstance(loaded_menu, dict) or not all(
        isinstance(name, str)
        and bool(name.strip())
        and isinstance(price, (int, float))
        and not isinstance(price, bool)
        and math.isfinite(price)
        and price >= 0
        for name, price in loaded_menu.items()
    ):
        raise ValueError("Menu must map item names to non-negative prices.")
    menu.clear()
    menu.update(loaded_menu)


def daily_revenue():
    """Return the total value of delivered orders."""
    return sum(
        order["total"]
        for order in orders.values()
        if order["status"] == "delivered"
    )


def backup_orders(file="orders.json"):
    """Save orders as JSON rather than an unsafe pickle stream."""
    with Path(file).open("w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file, indent=2)


def restore_orders(file="orders.json"):
    """Restore orders from JSON after validating its structure."""
    with Path(file).open("r", encoding="utf-8") as backup_file:
        restored = json.load(backup_file)
    if not isinstance(restored, dict):
        raise ValueError("Order backup must contain a JSON object.")
    validated_orders = {}
    for order_id, order in restored.items():
        try:
            numeric_order_id = int(order_id)
        except (TypeError, ValueError) as exc:
            message = f"Invalid order ID in backup: {order_id}"
            raise ValueError(message) from exc
        if numeric_order_id < 1:
            raise ValueError(f"Invalid order ID in backup: {order_id}")
        if numeric_order_id in validated_orders:
            raise ValueError(f"Duplicate order ID in backup: {order_id}")
        if not isinstance(order, dict) or not {
            "customer", "items", "total", "status"
        }.issubset(order):
            raise ValueError(f"Invalid order record: {order_id}")
        customer = order["customer"]
        if not isinstance(customer, str) or not customer.strip():
            message = f"Invalid customer in backup for order {order_id}"
            raise ValueError(message)
        if not isinstance(order["items"], list) or not order["items"] or any(
            not isinstance(item, str) or not item for item in order["items"]
        ):
            raise ValueError(f"Invalid items in backup for order {order_id}")
        total = order["total"]
        if (
            not isinstance(total, (int, float))
            or isinstance(total, bool)
            or not math.isfinite(total)
            or total < 0
        ):
            raise ValueError(f"Invalid total in backup for order {order_id}")
        if (
            not isinstance(order["status"], str)
            or order["status"] not in VALID_STATUSES
        ):
            raise ValueError(f"Invalid status in backup for order {order_id}")
        validated_orders[numeric_order_id] = order
    orders.clear()
    orders.update(validated_orders)
    id_counter["next"] = max(orders, default=0) + 1


def print_queue():
    """Print the current order queue."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    print(f"Order queue at {timestamp}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"], order["total"])


def main():
    """Run a small example of order processing and persistence."""
    read_menu_config()
    first_order = create_order("Asha", ["pizza", "coke"])
    second_order = create_order("Ravi", ["burger"])
    update_order_status(first_order, "delivered")
    update_order_status(second_order, "cooking")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()


if __name__ == "__main__":
    main()
