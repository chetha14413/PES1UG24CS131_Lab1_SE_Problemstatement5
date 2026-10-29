# Static Code Analysis Issue Log

The line references below refer to the original `before/delivery_system.py` supplied for the lab. Issues are ordered from high to medium severity, followed by lower-severity correctness and maintainability issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe deserialization with `pickle.load` | Security (High) | 2, 44 | Loading an untrusted pickle file can execute attacker-controlled code. | Replace pickle persistence with JSON and validate restored records. |
| Broad exception handling and silent failure | Quality / Reliability (High) | 24–28 | `except:` catches nearly every exception and suppresses invalid IDs or other defects, hiding failures. | Validate order IDs and status values and raise explicit exceptions. |
| Mutable default argument | Correctness (Medium) | 12 | `order_history=[]` is created once and reused across calls, leading to hidden state leakage. | Use `None` as the default and append only when a history list is explicitly passed. |
| Unvalidated status values | Correctness (Medium) | 22–25, 54 | An invalid status such as `teleported` is accepted, corrupting order state. | Check against the set of valid statuses before updating. |
| Unknown dishes silently charged a default price | Business logic (Medium) | 15 | `menu.get(i, 99)` allows nonexistent items and silently bills an arbitrary amount. | Reject items not present in the menu. |
| File handles not reliably closed | Reliability / Style (Medium) | 30–34, 41–47 | Menu, backup, and restore file handles are not managed consistently, and exceptions may leave handles open. | Use `with` context managers and explicit UTF-8 text handling. |
| Invalid or empty orders accepted | Correctness (Medium) | 13–18, 52 | An empty customer name and empty item list can be turned into an order. | Validate a non-empty customer name and at least one known item. |
| Non-PEP 8 function naming and formatting | Style (Low) | 49, throughout | `printQueue` and compressed formatting do not follow normal Python naming and style conventions. | Rename to `print_queue` and format consistently; verify with Flake8. |
| Script executes on import | Maintainability (Low) | 67 | Calling `main()` unconditionally causes side effects when imported for tests or reuse. | Guard execution with `if __name__ == "__main__":`. |
| Redundant revenue loop | Maintainability (Low) | 36–40 | The accumulation loop can be expressed more clearly using `sum`. | Use a generator expression with `sum`. |

## Fixes applied

- Replaced unsafe pickle persistence with JSON.
- Replaced the mutable `order_history` default with `None`.
- Validated customers, item names, order IDs, and allowed statuses.
- Replaced bare and silent exception handling with explicit errors.
- Used context managers for file operations.
- Added JSON, menu, and backup structure validation.
- Adopted `snake_case`, consistent formatting, and a main guard.
