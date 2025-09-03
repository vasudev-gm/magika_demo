# Test Infrastructure for Magika Demo

This directory contains tests for the Magika Demo Django application.

## Test Structure

- `test_sanity.py` - Basic sanity tests for Django setup and configuration
- `test_api.py` - API endpoint tests for the Django Ninja API
- `test_magika_integration.py` - Tests for Magika file type detection functionality

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test tests.test_api

# Run with verbose output
python manage.py test --verbosity=2
```

## Test Files

Test files are created to simulate various file types for upload testing.