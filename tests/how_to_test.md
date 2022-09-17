# How To Test

## Python

### Run Tests

This project uses `pytest` to test python modules.

`pip install pytest`

You will also need the validators module

`pip install validators`

To run all tests navigate to the root of the repo and run the follow:

`pytest`

## Add new tests

Add new tests to the `tests` folder. 

Ensure you name your file `xxxx_test.py` for it to be run

Ensure all test function to be executed by pytest are named `test_xxxx()` otherwise they will not be called.  You can add helper function without this naming convention in teh same files.

Common helper functions (such as csv validators) should be added to conftest.py

