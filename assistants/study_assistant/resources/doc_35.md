We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

##### Contribute

* [Philosophy](#philosophy)
* [Getting started](#getting-started)
* [Quick fix: submit a bugfix](#quick-fix%3A-submit-a-bugfix)
* [Full development setup](#full-development-setup)
* [Development environment](#development-environment)
* [Repository structure](#repository-structure)
* [Development workflow](#development-workflow)
* [Testing requirements](#testing-requirements)
* [Code quality standards](#code-quality-standards)
* [Manual formatting and linting](#manual-formatting-and-linting)
* [Contribution guidelines](#contribution-guidelines)
* [Backwards compatibility](#backwards-compatibility)
* [Bugfixes](#bugfixes)
* [New features](#new-features)
* [Security guidelines](#security-guidelines)
* [Testing and validation](#testing-and-validation)
* [Running tests locally](#running-tests-locally)
* [Test writing guidelines](#test-writing-guidelines)
* [Getting help](#getting-help)

[Contribute](/oss/python/contributing/documentation)

# Contributing to code

Code contributions are always welcome! Whether you’re fixing bugs, adding features, or improving performance, your contributions help deliver a better developer experience for thousands of developers.

Before submitting large **new features or refactors**, please first discuss your ideas in [the forum](https://forum.langchain.com/). This ensures alignment with project goals and prevents duplicate work.This does not apply to bugfixes or small improvements, which you can contribute directly via pull requests. Be sure to link any relevant issues in your PR description. Use to automatically close issues when the PR is merged.New integrations should follow the [integration guidelines](/oss/python/contributing#add-a-new-integration).

## Philosophy

Aim to follow these core principles for all code contributions:

[## Backwards compatibility

Maintain stable public interfaces and avoid breaking changes](#backwards-compatibility)[## Testing first

Every change must include comprehensive tests to verify correctness and prevent regressions](#testing-requirements)[## Code quality

Follow consistent style, documentation, and architecture patterns](#code-quality-standards)[## Security focused

Prioritize secure coding practices and vulnerability prevention](#security-guidelines)

---

## [​](#getting-started) Getting started

### [​](#quick-fix%3A-submit-a-bugfix) Quick fix: submit a bugfix

For simple bugfixes, you can get started immediately:

1

Fork the repository

Fork the [LangChain](https://github.com/langchain-ai/langchain) or [LangGraph](https://github.com/langchain-ai/langgraph) repo to your

2

Clone and setup

Copy

Ask AI

```
git clone https://github.com/your-username/name-of-forked-repo.git git  clone https://github.com/your-username/name-of-forked-repo.git # For instance, for LangChain:# For instance, for LangChain:git clone https://github.com/parrot123/langchain.git git  clone https://github.com/parrot123/langchain.git # For LangGraph:# For LangGraph:git clone https://github.com/parrot123/langgraph.git git  clone https://github.com/parrot123/langgraph.git
```

Copy

Ask AI

```
# Inside your repo, install dependencies# Inside your repo, install dependenciesuv sync --all-groups uv  sync --all-groups
```

You will need to install [`uv`](https://docs.astral.sh/uv/) if you haven’t previously.

3

Create a branch

Copy

Ask AI

```
git checkout -b your-username/short-bugfix-name git  checkout -b your-username/short-bugfix-name
```

4

Make your changes

Fix the bug while following our [code quality standards](#code-quality-standards)

5

Add tests

Include [unit tests](#test-writing-guidelines) that fail without your fix. This allows us to verify the bug is resolved and prevents regressions

6

Run tests

Ensure all tests pass locally before submitting your PR

Copy

Ask AI

```
make lint make  lint make test make  test # For bugfixes involving integrations, also run:# For bugfixes involving integrations, also run: make integration_tests make  integration_tests
```

7

Submit a pull request

Follow the PR template provided. If applicable, reference the issue you’re fixing using a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) (e.g. `Fixes #123`).

### [​](#full-development-setup) Full development setup

For ongoing development or larger contributions:

1

Development environment

Set up your environment following our [setup guide](#development-environment) below

2

Repository structure

Understand the [repository structure](#repository-structure) and package organization

3

Development workflow

Learn our [development workflow](#development-workflow) including testing and linting

4

Contribution guidelines

Review our [contribution guidelines](#contribution-guidelines) for features, bugfixes, and integrations

### [​](#development-environment) Development environment

Our Python projects use [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for dependency management. Make sure you have the latest version installed.

Set up a development environment for the package(s) you’re working on.

* LangChain
* LangGraph

Core abstractions

For changes to `langchain-core`:

Copy

Ask AI

```
cd libs/core cd libs/coreuv sync --all-groups uv  sync --all-groups make test # Ensure tests pass before starting development make  test  # Ensure tests pass before starting development
```

Main package

For changes to `langchain`:

Copy

Ask AI

```
cd libs/langchain cd libs/langchainuv sync --all-groups uv  sync --all-groups make test # Ensure tests pass before starting development make  test  # Ensure tests pass before starting development
```

Partner packages

For changes to [partner integrations](/oss/python/integrations/providers/overview):

Copy

Ask AI

```
cd libs/partners/langchain-{partner} cd libs/partners/langchain-{partner}uv sync --all-groups uv  sync --all-groups make test # Ensure tests pass before starting development make  test  # Ensure tests pass before starting development
```

Community packages

For changes to community integrations (located in a [separate repo](https://github.com/langchain-ai/langchain-community)):

Copy

Ask AI

```
cd libs/community/langchain_community/path/to/integration cd libs/community/langchain_community/path/to/integrationuv sync --all-groups uv  sync --all-groups make test # Ensure tests pass before starting development make  test  # Ensure tests pass before starting development
```

---

## [​](#repository-structure) Repository structure

* LangChain
* LangGraph

LangChain is organized as a monorepo with multiple packages:

Core packages

* **[`langchain`](https://github.com/langchain-ai/langchain/tree/master/libs/langchain#readme)** (located in `libs/langchain/`): Main package with chains, agents, and retrieval logic
* **[`langchain-core`](https://github.com/langchain-ai/langchain/tree/master/libs/core#readme)** (located in `libs/core/`): Base interfaces and core abstractions

Partner packages

Located in `libs/partners/`, these are independently versioned packages for specific integrations. For example:

* **[`langchain-openai`](https://github.com/langchain-ai/langchain/tree/master/libs/partners/openai#readme)**: [OpenAI](/oss/python/integrations/providers/openai) integrations
* **[`langchain-anthropic`](https://github.com/langchain-ai/langchain/tree/master/libs/partners/anthropic#readme)**: [Anthropic](/oss/python/integrations/providers/anthropic) integrations
* **[`langchain-google-genai`](https://github.com/langchain-ai/langchain-google/)**: [Google Generative AI](/oss/python/integrations/chat/google_generative_ai) integrations

Many partner packages are in external repositories. Please check the [list of integrations](/oss/python/integrations/providers/overview) for details.

Supporting packages

* **[`langchain-text-splitters`](https://github.com/langchain-ai/langchain/tree/master/libs/text-splitters#readme)**: Text splitting utilities
* **[`langchain-standard-tests`](https://github.com/langchain-ai/langchain/tree/master/libs/standard-tests#readme)**: Standard test suites for integrations
* **[`langchain-cli`](https://github.com/langchain-ai/langchain/tree/master/libs/cli#readme)**: Command line interface
* **[`langchain-community`](https://github.com/langchain-ai/langchain-community)**: Community maintained integrations (located in a separate repo)

---

## [​](#development-workflow) Development workflow

### [​](#testing-requirements) Testing requirements

Directories are relative to the package you’re working in.

Every code change must include comprehensive tests.

1

Unit tests

**Location**: `tests/unit_tests/`**Requirements**:

* No network calls allowed
* Test all code paths including edge cases
* Use mocks for external dependencies

Copy

Ask AI

```
make test make  test# Or directly:# Or directly:uv run --group test pytest tests/unit_tests uv  run --group  test  pytest tests/unit_tests
```

2

Integration tests

Integration tests require access to external services/ provider APIs (which can cost money) and therefore are not run by default.Not every code change will require an integration test, but keep in mind that we’ll require/ run integration tests separately as apart of our review process.**Location**: `tests/integration_tests/`**Requirements**:

* Test real integrations with external services
* Use environment variables for API keys
* Skip gracefully if credentials unavailable

Copy

Ask AI

```
make integration_tests make  integration_tests
```

3

Test quality checklist

* Tests fail when your code is broken
* Edge cases and error conditions are tested
* Proper use of fixtures and mocks

### [​](#code-quality-standards) Code quality standards

Quality requirements:

* Type hints
* Documentation
* Code style

**Required**: Complete type annotations for all functions

Copy

Ask AI

```
def process_documents(def  process_documents( docs: list[Document],  docs: list[Document], processor: DocumentProcessor,  processor: DocumentProcessor, *, *, batch_size: int = 100  batch_size: int =  100) -> ProcessingResult:) -> ProcessingResult: """Process documents in batches. """Process documents in batches.  Args: Args: docs: List of documents to process. docs: List of documents to process. processor: Document processing instance. processor: Document processing instance. batch_size: Number of documents per batch. batch_size: Number of documents per batch.  Returns: Returns: Processing results with success/failure counts. Processing results with success/failure counts.  """  """
```

### [​](#manual-formatting-and-linting) Manual formatting and linting

Code formatting and linting are enforced via CI/CD. Run these commands before committing to ensure your code passes checks.

Run formatting and linting:

1

Format code

Copy

Ask AI

```
make format make  format
```

2

Run linting checks

Copy

Ask AI

```
make lint make  lint
```

3

Verify changes

Both commands will show you any formatting or linting issues that need to be addressed before committing.

---

## [​](#contribution-guidelines) Contribution guidelines

### [​](#backwards-compatibility) Backwards compatibility

Breaking changes to public APIs are not allowed except for critical security fixes.See our [versioning policy](/oss/python/versioning) for details on major version releases.

Maintain compatibility:

Stable interfaces

**Always preserve**:

* Function signatures and parameter names
* Class interfaces and method names
* Return value structure and types
* Import paths for public APIs

Safe changes

**Acceptable modifications**:

* Adding new optional parameters
* Adding new methods to classes
* Improving performance without changing behavior
* Adding new modules or functions

Before making changes

* **Would this break existing user code?**
* Check if your target is public
* If needed, is it exported in `__init__.py`?
* Are there existing usage patterns in tests?

### [​](#bugfixes) Bugfixes

For bugfix contributions:

1

Reproduce the issue

Create a minimal test case that demonstrates the bug. Maintainers and other contributors should be able to run this test and see the failure without additional setup or modification

2

Write failing tests

Add unit tests that would fail without your fix

3

Implement the fix

Make the **minimal change necessary** to resolve the issue

4

Verify the fix

Ensure that tests pass and no regressions are introduced

5

Document the change

Update docstrings if behavior changes, add comments for complex logic

### [​](#new-features) New features

We aim to keep the bar high for new features. We generally don’t accept new core abstractions, changes to infra, changes to dependencies, or new agents/chains from outside contributors without an existing issue that demonstrates an acute need for them. In general, feature contribution requirements include:

1

Design discussion

Open an issue describing:

* The problem you’re solving
* Proposed API design
* Expected usage patterns

2

Implementation

* Follow existing code patterns
* Include comprehensive tests and documentation
* Consider security implications

3

Integration considerations

* How does this interact with existing features?
* Are there performance implications?
* Does this introduce new dependencies?

We will reject features that are likely to lead to security vulnerabilities or reports.

### [​](#security-guidelines) Security guidelines

Security is paramount. Never introduce vulnerabilities or unsafe patterns.

Security checklist:

Input validation

* Validate and sanitize all user inputs
* Properly escape data in templates and queries
* Never use `eval()`, `exec()`, or `pickle` on user data, as this can lead to arbitrary code execution vulnerabilities

Error handling

* Use specific exception types
* Don’t expose sensitive information in error messages
* Implement proper resource cleanup

Dependencies

* Avoid adding hard dependencies
* Keep optional dependencies minimal
* Review third-party packages for security issues

---

## [​](#testing-and-validation) Testing and validation

### [​](#running-tests-locally) Running tests locally

Before submitting your PR, ensure you have completed the following steps. Note that the requirements differ slightly between LangChain and LangGraph.

* LangChain
* LangGraph

1

Unit tests

Copy

Ask AI

```
make test make  test
```

All unit tests must pass

2

Integration tests

Copy

Ask AI

```
make integration_tests make  integration_tests
```

(Run if your changes affect integrations)

3

Copy

Ask AI

```
make format make  format make lint make  lint
```

Code must pass all style checks

4

Type checking

Copy

Ask AI

```
make type_check make  type_check
```

All type hints must be valid

5

PR submission

Push your branch and open a pull request. Follow the provided form template. Note related issues using a [closing keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword). After submitting, wait, and check to ensure the CI checks pass. If any checks fail, address the issues promptly - maintainers may close PRs that do not pass CI within a reasonable timeframe.

### [​](#test-writing-guidelines) Test writing guidelines

In order to write effective tests, there’s a few good practices to follow:

* Use natural language to describe the test in docstrings
* Use descriptive variable names
* Be exhaustive with assertions

* Unit tests
* Integration tests
* Mock usage

Copy

Ask AI

```
def test_document_processor_handles_empty_input(): def  test_document_processor_handles_empty_input(): """Test processor gracefully handles empty document list.""" """Test processor gracefully handles empty document list.""" processor = DocumentProcessor()  processor = DocumentProcessor()  result = processor.process([])  result = processor.process([])  assert result.success  assert result.success assert result.processed_count == 0  assert result.processed_count ==  0 assert len(result.errors) == 0  assert  len(result.errors) ==  0
```

## [​](#getting-help) Getting help

Our goal is to have the most accessible developer setup possible. Should you experience any difficulty getting setup, please ask in the [community slack](https://www.langchain.com/join-community) or open a [forum post](https://forum.langchain.com/).

You’re now ready to contribute high-quality code to LangChain!

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/contributing/code.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Contributing to documentation](/oss/python/contributing/documentation)[Contributing integrations](/oss/python/contributing/integrations-langchain)