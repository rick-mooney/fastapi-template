## API Tests

For API tests, we use pytest.

# Writing Tests

Strive to create tests that run each part of logic in the api code. Don't write tests for 3rd party packages i.e. schema validation is handled by FastAPI, so you dont need to write tests to check for payload correctness

After creating a new API endpoint, follow steps below:

- If you have created a new router, be sure to write your tests in a new test file in `app/api/v1/routers/tests` with the format `test_{routerName}.py` and import pytest
- give your test function a descriptive name that begins with `test_` (i.e. `test_sorted_result_history.py`)
- Some tests require data to be seeded in the db. In this case, you can create a new python object in `mock.py` to represent the db table. Then add the mock data to the `seed_database` function in `conftest.py`.

# Running API Tests

- NOTE: you can override ENV variables by adding them before pytest. Here `TEST_RUN` is being used to select the test db. If there is a use case for loading multiple env vars, we could switch to load_env to dynamically load different env files during tests
- Run all tests `TEST_RUN=TRUE pytest -s`
- Run specific test file `TEST_RUN=TRUE pytest app/api/v1/routers/tests/test_users.py -s`
- Run function in a file `TEST_RUN=TRUE pytest app/api/v1/routers/tests/test_auth.py::test_login -s`
- Note: the `-s` shows the standard out in the terminal for successful tests
- There are also tons of other interesting ways to run tests if you have a specific use case: `https://docs.pytest.org/en/7.1.x/how-to/usage.html`
