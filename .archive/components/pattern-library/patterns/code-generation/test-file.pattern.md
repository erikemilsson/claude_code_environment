# Pattern: Test File

## Metadata
- **ID**: pattern-code-test-file
- **Version**: 1.0.0
- **Category**: code-generation
- **Difficulty Range**: 4-6 (test creation tasks)

## Triggers
Keywords that suggest this pattern applies:
- create test
- write test
- test file
- unit test
- pytest
- test coverage
- test case

File types: test_*.py, *_test.py

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| module_under_test | string | yes | Module/file being tested |
| test_framework | enum | no | pytest/unittest (default: pytest) |
| class_or_function | string | yes | What is being tested |
| test_scenarios | string | yes | List of test cases (one per line) |
| use_fixtures | boolean | no | Include pytest fixtures (default: true) |
| use_mocks | boolean | no | Include mocking examples (default: false) |
| use_parametrize | boolean | no | Include parametrized tests (default: false) |

## Pre-Conditions
- [ ] Module under test exists
- [ ] Test framework installed (pytest or unittest)
- [ ] Test file follows naming convention (test_*.py or *_test.py)
- [ ] Test scenarios cover happy path and edge cases

## Template

### Pytest Style (Default)
```python
"""Tests for {{module_under_test}}.{{class_or_function}}."""

import pytest
{{#if use_mocks}}
from unittest.mock import Mock, patch
{{/if}}

from {{module_under_test}} import {{class_or_function}}


{{#if use_fixtures}}
@pytest.fixture
def {{fixture_name}}():
    """Fixture for {{fixture_description}}."""
    {{fixture_setup}}
    yield {{fixture_object}}
    {{fixture_teardown}}
{{/if}}


{{#if use_parametrize}}
@pytest.mark.parametrize("{{param_names}}", [
    {{test_parameters}}
])
def test_{{test_name}}_parametrized({{param_names}}):
    """Test {{test_description}} with multiple inputs."""
    {{test_body}}
{{/if}}


def test_{{test_name}}_happy_path():
    """Test {{test_description}} with valid input."""
    # Arrange
    {{setup_code}}

    # Act
    result = {{function_call}}

    # Assert
    assert {{assertion}}


def test_{{test_name}}_edge_case():
    """Test {{test_description}} with edge case input."""
    # Arrange
    {{edge_case_setup}}

    # Act & Assert
    with pytest.raises({{ExpectedException}}):
        {{function_call}}


{{#if use_mocks}}
@patch('{{module_under_test}}.{{dependency}}')
def test_{{test_name}}_with_mock(mock_{{dependency}}):
    """Test {{test_description}} with mocked dependency."""
    # Arrange
    mock_{{dependency}}.return_value = {{mock_return}}

    # Act
    result = {{function_call}}

    # Assert
    assert {{assertion}}
    mock_{{dependency}}.assert_called_once_with({{expected_args}})
{{/if}}
```

### Unittest Style
```python
"""Tests for {{module_under_test}}.{{class_or_function}}."""

import unittest
{{#if use_mocks}}
from unittest.mock import Mock, patch
{{/if}}

from {{module_under_test}} import {{class_or_function}}


class Test{{class_or_function}}(unittest.TestCase):
    """Test cases for {{class_or_function}}."""

    def setUp(self):
        """Set up test fixtures."""
        {{setup_code}}

    def tearDown(self):
        """Clean up after tests."""
        {{cleanup_code}}

    def test_{{test_name}}_happy_path(self):
        """Test {{test_description}} with valid input."""
        # Arrange
        {{arrange_code}}

        # Act
        result = {{act_code}}

        # Assert
        self.assertEqual(result, {{expected}})

    def test_{{test_name}}_edge_case(self):
        """Test {{test_description}} with edge case input."""
        # Arrange
        {{edge_case_setup}}

        # Act & Assert
        with self.assertRaises({{ExpectedException}}):
            {{function_call}}


if __name__ == '__main__':
    unittest.main()
```

## Post-Conditions
- [ ] All test scenarios from requirements covered
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Test names are descriptive
- [ ] Each test tests one thing
- [ ] Tests are independent (no shared state)
- [ ] Tests can run in any order
- [ ] All tests pass

## Anti-Patterns
**DON'T do this:**
- Test implementation details instead of behavior
- Multiple assertions testing different things in one test
- Tests that depend on execution order
- Shared mutable state between tests
- Tests that access real databases/network
- Overly complex test setup (suggests code smell)
- No edge case or error testing
- Vague test names like test_1, test_2

**WHY**:
- Implementation-focused tests break when refactoring
- Multiple assertions make failures unclear
- Order-dependent tests are fragile
- Shared state causes cascading failures
- Real I/O makes tests slow and unreliable
- Complex setup indicates code needs refactoring
- Edge cases often where bugs hide
- Vague names don't document behavior

## Examples

### Example 1: Simple Function Tests
**Input:**
```
module_under_test: utils.calculator
test_framework: pytest
class_or_function: calculate_total
test_scenarios: |
  - Happy path: sum list of positive numbers
  - Empty list: should raise ValueError
  - Non-numeric: should raise TypeError
use_fixtures: false
use_mocks: false
use_parametrize: true
```

**Output:**
```python
"""Tests for utils.calculator.calculate_total."""

import pytest

from utils.calculator import calculate_total


@pytest.mark.parametrize("numbers,expected", [
    ([1, 2, 3], 6),
    ([0], 0),
    ([1.5, 2.5], 4.0),
    ([100, 200, 300], 600),
])
def test_calculate_total_parametrized(numbers, expected):
    """Test calculate_total with multiple valid inputs."""
    result = calculate_total(numbers)
    assert result == expected


def test_calculate_total_happy_path():
    """Test calculate_total with valid list of numbers."""
    # Arrange
    numbers = [10, 20, 30]

    # Act
    result = calculate_total(numbers)

    # Assert
    assert result == 60


def test_calculate_total_empty_list():
    """Test calculate_total with empty list raises ValueError."""
    # Arrange
    numbers = []

    # Act & Assert
    with pytest.raises(ValueError, match="Cannot calculate total of empty list"):
        calculate_total(numbers)


def test_calculate_total_non_numeric():
    """Test calculate_total with non-numeric values raises TypeError."""
    # Arrange
    numbers = [1, 2, "three"]

    # Act & Assert
    with pytest.raises(TypeError):
        calculate_total(numbers)
```

### Example 2: Class Tests with Fixtures
**Input:**
```
module_under_test: models.bank_account
test_framework: pytest
class_or_function: BankAccount
test_scenarios: |
  - Initialize account correctly
  - Deposit increases balance
  - Withdraw decreases balance
  - Withdraw more than balance raises ValueError
  - Negative deposit raises ValueError
use_fixtures: true
use_mocks: false
use_parametrize: false
```

**Output:**
```python
"""Tests for models.bank_account.BankAccount."""

import pytest

from models.bank_account import BankAccount


@pytest.fixture
def bank_account():
    """Fixture for BankAccount with initial balance."""
    return BankAccount(account_number="12345", balance=100.0, owner="John Doe")


def test_bank_account_initialization():
    """Test BankAccount initializes with correct attributes."""
    # Arrange & Act
    account = BankAccount(
        account_number="12345",
        balance=100.0,
        owner="John Doe"
    )

    # Assert
    assert account.account_number == "12345"
    assert account.balance == 100.0
    assert account.owner == "John Doe"


def test_deposit_increases_balance(bank_account):
    """Test deposit method increases account balance."""
    # Arrange
    initial_balance = bank_account.balance

    # Act
    bank_account.deposit(50.0)

    # Assert
    assert bank_account.balance == initial_balance + 50.0


def test_withdraw_decreases_balance(bank_account):
    """Test withdraw method decreases account balance."""
    # Arrange
    initial_balance = bank_account.balance

    # Act
    bank_account.withdraw(30.0)

    # Assert
    assert bank_account.balance == initial_balance - 30.0


def test_withdraw_insufficient_funds(bank_account):
    """Test withdraw with amount exceeding balance raises ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Insufficient funds"):
        bank_account.withdraw(200.0)


def test_deposit_negative_amount(bank_account):
    """Test deposit with negative amount raises ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        bank_account.deposit(-50.0)
```

### Example 3: Tests with Mocking
**Input:**
```
module_under_test: services.user_service
test_framework: pytest
class_or_function: UserService
test_scenarios: |
  - get_user calls database correctly
  - get_user returns None for missing user
  - create_user saves to database
use_fixtures: true
use_mocks: true
use_parametrize: false
```

**Output:**
```python
"""Tests for services.user_service.UserService."""

import pytest
from unittest.mock import Mock, patch

from services.user_service import UserService


@pytest.fixture
def user_service():
    """Fixture for UserService with mocked database."""
    mock_db = Mock()
    return UserService(database=mock_db)


def test_get_user_calls_database(user_service):
    """Test get_user calls database with correct user_id."""
    # Arrange
    user_id = 123
    user_service.database.query.return_value = {"id": 123, "name": "John"}

    # Act
    result = user_service.get_user(user_id)

    # Assert
    user_service.database.query.assert_called_once_with("users", id=user_id)
    assert result["id"] == 123


def test_get_user_missing_user(user_service):
    """Test get_user returns None when user not found."""
    # Arrange
    user_id = 999
    user_service.database.query.return_value = None

    # Act
    result = user_service.get_user(user_id)

    # Assert
    assert result is None


@patch('services.user_service.datetime')
def test_create_user_saves_to_database(mock_datetime, user_service):
    """Test create_user saves new user with timestamp."""
    # Arrange
    mock_datetime.now.return_value = "2025-12-05"
    user_data = {"name": "Jane", "email": "jane@example.com"}

    # Act
    user_service.create_user(user_data)

    # Assert
    user_service.database.insert.assert_called_once()
    call_args = user_service.database.insert.call_args[0][1]
    assert call_args["name"] == "Jane"
    assert call_args["created_at"] == "2025-12-05"
```

## Usage Notes

### Test Structure (AAA Pattern)
1. **Arrange**: Set up test data and conditions
2. **Act**: Execute the code under test
3. **Assert**: Verify the results

### Naming Conventions
```
test_<function_name>_<scenario>

Examples:
- test_calculate_total_happy_path
- test_calculate_total_empty_list
- test_bank_account_insufficient_funds
```

### Pytest vs Unittest
**Pytest (Recommended):**
- Simpler syntax
- Better fixtures
- Parametrization support
- More powerful assertions

**Unittest:**
- Standard library (no install)
- More verbose
- Class-based structure

### Fixtures Best Practices
- One fixture per concept
- Fixture scope: function (default), class, module, session
- Use `yield` for cleanup
- Compose fixtures (fixtures can use other fixtures)

### Mocking Guidelines
- Mock external dependencies (databases, APIs, file system)
- Don't mock code under test
- Verify mock calls to ensure correct integration
- Use `patch` for module-level mocking

## Test Coverage Goals
- **Minimum**: Happy path + major edge cases (60%+)
- **Good**: All public methods + error cases (80%+)
- **Excellent**: All branches + edge cases (90%+)

## Related Patterns
- `python-function.pattern.md` - Functions to test
- `python-class.pattern.md` - Classes to test

## Testing Checklist
- [ ] All public methods/functions tested
- [ ] Happy path covered
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Tests are independent
- [ ] Tests are fast (<1s each)
- [ ] Test names describe behavior
- [ ] All tests pass
