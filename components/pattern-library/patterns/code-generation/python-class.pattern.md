# Pattern: Python Class

## Metadata
- **ID**: pattern-code-python-class
- **Version**: 1.0.0
- **Category**: code-generation
- **Difficulty Range**: 4-6 (class implementation tasks)

## Triggers
Keywords that suggest this pattern applies:
- python class
- create class
- implement class
- add class
- object oriented
- dataclass
- model

File types: .py

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| class_name | string | yes | Name of class (PascalCase) |
| description | string | yes | What the class represents |
| base_classes | string | no | Parent classes to inherit from (comma-separated) |
| attributes | string | yes | Instance attributes with types (one per line) |
| use_dataclass | boolean | no | Use @dataclass decorator (default: false) |
| include_str | boolean | no | Include __str__ method (default: true) |
| include_repr | boolean | no | Include __repr__ method (default: true) |
| include_eq | boolean | no | Include __eq__ method (default: false) |

## Pre-Conditions
- [ ] Class name follows PascalCase convention
- [ ] Attribute types are valid Python type hints
- [ ] Base classes exist if inheritance specified
- [ ] Dataclass usage appropriate for use case

## Template

### Standard Class
```python
{{#if base_classes}}
class {{class_name}}({{base_classes}}):
{{else}}
class {{class_name}}:
{{/if}}
    """{{description}}

    Attributes:
        {{attribute_docs}}
    """

    def __init__(self, {{init_parameters}}):
        """Initialize {{class_name}}.

        Args:
            {{init_parameter_docs}}
        """
        {{attribute_assignments}}

    {{#if include_str}}
    def __str__(self) -> str:
        """Return string representation."""
        return f"{{class_name}}({{str_attributes}})"
    {{/if}}

    {{#if include_repr}}
    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"{{class_name}}({{repr_attributes}})"
    {{/if}}

    {{#if include_eq}}
    def __eq__(self, other: object) -> bool:
        """Check equality with another instance."""
        if not isinstance(other, {{class_name}}):
            return NotImplemented
        return {{equality_checks}}
    {{/if}}
```

### Dataclass Version
```python
from dataclasses import dataclass

@dataclass
{{#if base_classes}}
class {{class_name}}({{base_classes}}):
{{else}}
class {{class_name}}:
{{/if}}
    """{{description}}

    Attributes:
        {{attribute_docs}}
    """
    {{dataclass_attributes}}
```

## Post-Conditions
- [ ] Class has complete docstring
- [ ] All attributes have type hints
- [ ] __init__ properly initializes all attributes
- [ ] Special methods (__str__, __repr__, etc.) implemented as needed
- [ ] Class follows single responsibility principle
- [ ] Unit tests exist or planned

## Anti-Patterns
**DON'T do this:**
- Missing docstring or incomplete attribute documentation
- No type hints on attributes
- Too many attributes (>10 suggests refactoring)
- Mutable default values in __init__ (def __init__(self, items=[]):)
- God objects (classes that do everything)
- Anemic domain model (classes with only getters/setters, no logic)
- Missing __repr__ (hard to debug)
- Implementing __eq__ without __hash__ when needed

**WHY**:
- Docstrings essential for understanding class purpose
- Type hints enable IDE support and type checking
- Too many attributes indicate poor cohesion
- Mutable defaults shared across instances (Python gotcha)
- God objects violate single responsibility
- Anemic models miss OOP benefits
- __repr__ critical for debugging
- __eq__ without __hash__ breaks dict/set usage

## Examples

### Example 1: Simple Data Class
**Input:**
```
class_name: User
description: Represents a user in the system
base_classes:
attributes: |
  name: str
  email: str
  age: int
use_dataclass: true
include_str: true
include_repr: true
include_eq: false
```

**Output:**
```python
from dataclasses import dataclass

@dataclass
class User:
    """Represents a user in the system.

    Attributes:
        name: User's full name
        email: User's email address
        age: User's age in years
    """
    name: str
    email: str
    age: int
```

### Example 2: Standard Class with Methods
**Input:**
```
class_name: BankAccount
description: Represents a bank account with balance tracking
base_classes:
attributes: |
  account_number: str
  balance: float
  owner: str
use_dataclass: false
include_str: true
include_repr: true
include_eq: true
```

**Output:**
```python
class BankAccount:
    """Represents a bank account with balance tracking.

    Attributes:
        account_number: Unique account identifier
        balance: Current account balance
        owner: Account owner's name
    """

    def __init__(self, account_number: str, balance: float, owner: str):
        """Initialize BankAccount.

        Args:
            account_number: Unique account identifier
            balance: Initial account balance
            owner: Account owner's name
        """
        self.account_number = account_number
        self.balance = balance
        self.owner = owner

    def __str__(self) -> str:
        """Return string representation."""
        return f"BankAccount({self.account_number}, ${self.balance:.2f})"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"BankAccount(account_number={self.account_number!r}, balance={self.balance!r}, owner={self.owner!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another instance."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return (
            self.account_number == other.account_number
            and self.balance == other.balance
            and self.owner == other.owner
        )

    def deposit(self, amount: float) -> None:
        """Deposit money into account.

        Args:
            amount: Amount to deposit

        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money from account.

        Args:
            amount: Amount to withdraw

        Raises:
            ValueError: If amount is negative or exceeds balance
        """
        if amount < 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

### Example 3: Inheritance Example
**Input:**
```
class_name: SavingsAccount
description: Bank account with interest calculation
base_classes: BankAccount
attributes: |
  interest_rate: float
use_dataclass: false
include_str: true
include_repr: true
include_eq: false
```

**Output:**
```python
class SavingsAccount(BankAccount):
    """Bank account with interest calculation.

    Attributes:
        interest_rate: Annual interest rate (e.g., 0.05 for 5%)
        (Inherited from BankAccount: account_number, balance, owner)
    """

    def __init__(
        self,
        account_number: str,
        balance: float,
        owner: str,
        interest_rate: float
    ):
        """Initialize SavingsAccount.

        Args:
            account_number: Unique account identifier
            balance: Initial account balance
            owner: Account owner's name
            interest_rate: Annual interest rate (e.g., 0.05 for 5%)
        """
        super().__init__(account_number, balance, owner)
        self.interest_rate = interest_rate

    def __str__(self) -> str:
        """Return string representation."""
        return f"SavingsAccount({self.account_number}, ${self.balance:.2f}, {self.interest_rate:.2%})"

    def __repr__(self) -> str:
        """Return detailed representation."""
        return (
            f"SavingsAccount(account_number={self.account_number!r}, "
            f"balance={self.balance!r}, owner={self.owner!r}, "
            f"interest_rate={self.interest_rate!r})"
        )

    def apply_interest(self) -> None:
        """Apply interest to current balance."""
        interest = self.balance * self.interest_rate
        self.balance += interest
```

## Usage Notes

### When to Use Dataclass
**Use @dataclass when:**
- Class primarily holds data
- Need automatic __init__, __repr__, __eq__
- No complex initialization logic
- Attributes known at class definition

**Use standard class when:**
- Complex initialization needed
- Need custom __init__ logic
- Dynamic attributes
- Fine control over special methods

### Type Hints for Attributes
```python
from typing import Optional, List, Dict

class Example:
    name: str                    # Required string
    age: Optional[int] = None   # Optional with default
    tags: List[str]              # List of strings
    metadata: Dict[str, Any]     # Dictionary
```

### Special Methods Guide
- `__init__`: Always implement (unless using @dataclass)
- `__str__`: User-friendly string (for print())
- `__repr__`: Developer representation (for debugging)
- `__eq__`: Enable instance comparison
- `__hash__`: Required if using in sets/dict keys (with __eq__)
- `__len__`: If class is collection-like
- `__bool__`: If class has truthy/falsy semantics

### Class Complexity Guidelines
- **Simple (3-4)**: 3-5 attributes, simple __init__, basic methods
- **Moderate (4-6)**: 5-10 attributes, some business logic, inheritance
- **Complex (6-8)**: >10 attributes, complex logic → Consider refactoring

## Common Patterns

### Builder Pattern
For classes with many optional parameters:
```python
class UserBuilder:
    def __init__(self):
        self._user = User()

    def with_name(self, name: str):
        self._user.name = name
        return self

    def build(self) -> User:
        return self._user
```

### Factory Pattern
For complex object creation:
```python
class UserFactory:
    @staticmethod
    def create_admin(name: str) -> User:
        return User(name=name, role="admin", permissions=["all"])
```

## Related Patterns
- `python-function.pattern.md` - For class methods
- `test-file.pattern.md` - For testing classes
- Domain-specific class patterns (models, services, etc.)

## Testing Checklist
After creating class, ensure:
- [ ] Test __init__ with valid inputs
- [ ] Test __init__ with invalid inputs (if validation present)
- [ ] Test all public methods
- [ ] Test special methods (__str__, __eq__, etc.)
- [ ] Test inheritance if applicable
- [ ] Type hints verified with mypy
