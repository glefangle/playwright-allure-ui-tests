# UI Autotests -- saucedemo.com

UI test framework: Playwright (Python, sync API) + `pytest` + Page Object Model + Allure Report.

11 scenarios against [saucedemo.com](https://www.saucedemo.com): login (positive & negative),
product listing and sorting, cart management, full checkout flow.

## Architecture

```
ui-autotests/
├── src/
│   ├── config/              # pydantic-settings, .env-driven configuration
│   └── pages/               # Page Objects: locators + actions + page-level assertions
│       ├── base_page.py      # BasePage: open(), url
│       ├── login_page.py     # login(), expect_error()
│       ├── inventory_page.py # expect_loaded(), add_to_cart(), sort_by()
│       └── cart_page.py      # CartPage + CheckoutPage: fill_details(), finish()
├── tests/                   # Test scenarios only -- workflows expressed via page objects
│   ├── test_login.py        # 5 tests: success, locked-out user, 3x parametrized invalid
│   ├── test_inventory.py    # 4 tests: listing, sort low->high, sort high->low, cart badge
│   └── test_cart.py         # 2 tests: item appears in cart, full checkout flow
├── .github/workflows/ci.yml # CI: lint -> typecheck -> test -> Allure report -> Pages
├── pyproject.toml           # Ruff, Mypy, coverage config
├── Makefile                 # Standardised dev commands
└── pytest.ini
```

### Design principles

- **Page Object Model** -- tests read as business scenarios; selectors live in one place.
- **Role-based locators** (`get_by_role`, `get_by_text`) instead of brittle CSS/XPath where possible.
- **Automatic failure diagnostics** -- on every failure the report gets a full-page screenshot
  and a Playwright trace (open with `playwright show-trace <file>`): step-by-step DOM snapshots,
  network, console.
- **Flake control** -- `pytest-rerunfailures` retries; parallelization via `pytest -n auto`.

## Quick start

```bash
pip install -r requirements.txt -r requirements-dev.txt
playwright install chromium
cp .env.example .env
pytest                               # all tests, headless
pytest -m smoke                      # smoke subset
pytest --headed                      # watch the browser
pytest -n auto                       # parallel run
pytest --cov --cov-report=term-missing  # with coverage
allure serve allure-results          # local report
```

### Dev commands (via Make)

```bash
make lint        # ruff check + ruff format --check
make format      # ruff check --fix + ruff format
make typecheck   # mypy src tests
make test        # pytest
make test-cov    # pytest --cov
make report      # allure serve allure-results
make clean       # remove caches and generated artifacts
```

## Code quality toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| [Ruff](https://docs.astral.sh/ruff/) | Lint + format (replaces flake8, isort, black) | `pyproject.toml [tool.ruff]` |
| [Mypy](https://mypy.readthedocs.io/) | Static type checking | `pyproject.toml [tool.mypy]` |
| [pre-commit](https://pre-commit.com/) | Git hooks -- runs Ruff on every commit | `.pre-commit-config.yaml` |
| [pytest-cov](https://pytest-cov.readthedocs.io/) | Coverage reporting | `Makefile test-cov` |

Ruff rules: E/W (pycodestyle), F (pyflakes), I (isort), N (pep8-naming), UP (pyupgrade),
B (bugbear), C4 (comprehensions), SIM (simplify), PT (pytest-style), RUF (ruff-specific).

## Configuration

All settings come from environment variables or `.env` (see `.env.example`):

| Variable | Default | Purpose |
|----------|---------|---------|
| BASE_URL | https://www.saucedemo.com | Target environment |
| STANDARD_USER | standard_user | Valid login |
| LOCKED_USER | locked_out_user | Locked account (negative) |
| PASSWORD | secret_sauce | Shared password |
| HEADLESS | true | Run without a visible UI |
| SLOW_MO | 0 | Artificial delay, ms |
| TIMEOUT | 15 | Default action timeout, s |
| LOG_LEVEL | INFO | Logging verbosity |

## CI / Allure

Every push/PR runs: **lint -> typecheck -> test**. The Allure report (with trend history)
is published to GitHub Pages: `https://<owner>.github.io/<repo>/`. On failure, traces and
screenshots are also uploaded as CI artifacts.
