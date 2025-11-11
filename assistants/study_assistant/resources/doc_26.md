We've raised a $125M Series B to build the platform for agent engineering. [Read more](https://blog.langchain.com/series-b/?utm_medium=internal&utm_source=docs&utm_campaign=q4-2025_october-launch-week_aw).

[Docs by LangChain home page](/)

[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Deep Agents](/oss/python/deepagents/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

##### Contribute

* [Co-marketing](/oss/python/contributing/comarketing)

* [Getting started](#getting-started)
* [Quick edit: fix a typo](#quick-edit%3A-fix-a-typo)
* [Full development IDE setup](#full-development-ide-setup)
* [Documentation types](#documentation-types)
* [Conceptual guides](#conceptual-guides)
* [References](#references)
* [Writing standard](#writing-standard)
* [Mintlify components](#mintlify-components)
* [Page structure](#page-structure)
* [Co-locate Python and JavaScript/TypeScript content](#co-locate-python-and-javascript%2Ftypescript-content)
* [Localization](#localization)
* [Quality standards](#quality-standards)
* [General guidelines](#general-guidelines)
* [Accessibility requirements](#accessibility-requirements)
* [Testing and validation](#testing-and-validation)
* [In-code documentation](#in-code-documentation)
* [Language and style](#language-and-style)
* [Code examples](#code-examples)
* [Getting help](#getting-help)

[Contribute](/oss/python/contributing/documentation)

# Contributing to documentation

Accessible documentation is a vital part of LangChain. We welcome both documentation for new features/[integrations](/oss/python/contributing/publish-langchain#adding-documentation), as well as community improvements to existing docs.

We generally do not merge new tutorials from outside contributors without an acute need. If you feel that a certain topic is missing from docs or is not sufficiently covered, please [open a new issue](https://github.com/langchain-ai/docs/issues).

All documentation falls under one of four categories:

[## Conceptual guides

Explanations that provide deeper understanding and insights](#conceptual-guides)[## References

Technical descriptions of APIs and implementation details](#references)[## Tutorials (Learn)

Lessons that guide users through practical activities to build understanding](/oss/python/learn)

## How-to guides

Task-oriented instructions for users who know what they want to accomplish

---

## [​](#getting-started) Getting started

### [​](#quick-edit%3A-fix-a-typo) Quick edit: fix a typo

For simple changes like fixing typos, you can edit directly on GitHub without setting up a local development environment:

**Prerequisites:**

* A [GitHub](https://github.com/) account
* Basic familiarity of the [fork-and-pull workflow](https://graphite.dev/guides/understanding-git-fork-pull-request-workflow) for contributing

1

Find the page

Navigate to any documentation page, scroll to the bottom of the page, and click the link “Edit the source of this page on GitHub”

2

Fork the repository

GitHub will prompt you to fork the repository to your account. Make sure to fork into your

3

Make your changes

Correct the typo directly in GitHub’s web editor

4

Commit your changes

Click `Commit changes...` and give your commit a descriptive title like `fix(docs): summary of change`. If applicable, add an [extended description](https://www.gitkraken.com/learn/git/best-practices/git-commit-message#git-commit-message-structure)

5

Create pull request

GitHub will redirect you to create a pull request. Give it a title (often the same as the commit) and follow the PR template checklist, if present

Docs PRs are typically reviewed within a few days. Keep an eye on your PR to address any feedback from maintainers. Do not bump the PR unless you have new information to provide - maintainers will address it as their availability permits.

### [​](#full-development-ide-setup) Full development IDE setup

For larger changes or ongoing contributions, it’s important to set up a local development environment on your machine. Our documentation build pipeline offers local preview and live reload as you edit, important for ensuring your changes appear as intended before submitting. Please review the steps to set up your environment outlined in the docs repo [`README.md`](https://github.com/langchain-ai/docs?tab=readme-ov-file#contributing). 

---

## [​](#documentation-types) Documentation types

Where applicable, all documentation must have translations in both Python and JavaScript/TypeScript. See [our localization guide](#localization) for details.

### [​](#conceptual-guides) Conceptual guides

Conceptual guide cover core concepts abstractly, providing deep understanding.

Characteristics

* **Understanding-focused**: Explain why things work as they do
* **Broad perspective**: Higher and wider view than other types
* **Design-oriented**: Explain decisions and trade-offs
* **Context-rich**: Use analogies and comparisons

Tips

* Explain design decisions - *“why does concept X exist?”*
* Use analogies and reference alternatives
* Avoid blending in too much reference content
* Link to related tutorials and how-to guides
* Focus on the **“why”** rather than the “how”

Examples

[## Memory](/oss/python/concepts/memory)[## Context](/oss/python/concepts/context)

### [​](#references) References

Reference documentation contains detailed, low-level information describing exactly what functionality exists and how to use it. [## Python reference](https://reference.langchain.com/python/) A good reference should:

* Describe what exists (all parameters, options, return values)
* Be comprehensive and structured for easy lookup
* Serve as the authoritative source for technical details

Contributing to references

See the contributing guide for [Python reference docs](https://github.com/langchain-ai/docs/blob/main/reference/python/README.md).

LangChain reference best practices

* **Be consistent**; follow existing patterns for provider-specific documentation
* Include both basic usage (code snippets) and common edge cases/failure modes
* Note when features require specific versions

When to create new reference documentation

* New integrations or providers need dedicated reference pages
* Complex configuration options require detailed explanation
* API changes introduce new parameters or behavior
* Community frequently asks questions about specific functionality

---

## [​](#writing-standard) Writing standard

Reference documentation has different standards - see the [reference docs contributing guide](https://github.com/langchain-ai/docs/blob/main/reference/python/README.md) for details.

### [​](#mintlify-components) Mintlify components

Use appropriate [Mintlify components](https://mintlify.com/docs/text) to enhance readability:

* Callouts
* Structure
* Code

* for helpful supplementary information
* for important cautions and breaking changes
* for best practices and advice
* for neutral contextual information
* for success confirmations

### [​](#page-structure) Page structure

Every documentation page must begin with YAML frontmatter:

Copy

Ask AI

```
--- ---title: "Clear, specific title" title: "Clear, specific title" --- ---
```

### [​](#co-locate-python-and-javascript%2Ftypescript-content) Co-locate Python and JavaScript/TypeScript content

All documentation must be written in both Python and JavaScript/TypeScript when possible. To do so, we use a custom in-line syntax to differentiate between sections that should appear in one or both languages:

Copy

Ask AI

```
:::python:::pythonPython-specific content. In real docs, the preceding backslash (before `python`) is omitted.Python-specific content. In real docs, the preceding backslash (before ` python `) is omitted.:::::: :::js:::jsJavaScript/TypeScript-specific content. In real docs, the preceding backslash (before `js`) is omitted.JavaScript/TypeScript-specific content. In real docs, the preceding backslash (before ` js `) is omitted.:::::: Content for both languages (not wrapped)Content for both languages (not wrapped)
```

We don’t want a lack of parity to block contributions. If a feature is only available in one language, it’s okay to have documentation only in that language until the other language catches up. In such cases, please include a note indicating that the feature is not yet available in the other language.

If you need help translating content between Python and JavaScript/TypeScript, please ask in the [community slack](https://www.langchain.com/join-community) or tag a maintainer in your PR.

### [​](#localization) Localization

We are working to add support for other languages, thanks to our LangChain Ambassadors! 

---

## [​](#quality-standards) Quality standards

### [​](#general-guidelines) General guidelines

Avoid duplication

Multiple pages covering the same material are difficult to maintain and cause confusion. There should be only one canonical page for each concept or feature. Link to other guides instead of re-explaining.

Link frequently

Documentation sections don’t exist in a vacuum. Link to other sections frequently to allow users to learn about unfamiliar topics. This includes linking to API references and conceptual sections.

Be concise

Take a less-is-more approach. If another section with a good explanation exists, link to it rather than re-explain, unless your content presents a new angle.

### [​](#accessibility-requirements) Accessibility requirements

Ensure documentation is accessible to all users:

* Structure content for easy scanning with headers and lists
* Use specific, actionable link text instead of “click here”
* Include descriptive alt text for all images and diagrams

### [​](#testing-and-validation) Testing and validation

Before submitting documentation:

1

Test all code

Run all code examples to ensure they work correctly

2

Check formatting

Copy

Ask AI

```
make lint make  lint make format make  format
```

3

Build locally

Copy

Ask AI

```
docs build docs  build
```

Verify the build completes without errors

4

Review links

Check that all internal links work correctly

---

## [​](#in-code-documentation) In-code documentation

### [​](#language-and-style) Language and style

Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html) with complete type hints for all public functions.

Follow these standards for all documentation:

* **Voice**: Use second person (“you”) for instructions
* **Tense**: Use active voice and present tense
* **Clarity**: Write clear, direct language for technical audiences
* **Consistency**: Use consistent terminology throughout
* **Conciseness**: Keep sentences concise while providing necessary context

### [​](#code-examples) Code examples

Always test code examples before publishing. Never include real API keys or secrets.

Requirements for code examples:

1

Completeness

Include complete, runnable examples that users can copy and execute without errors

2

Realism

Use realistic data instead of placeholder values like “foo” or “example”

3

Error handling

Show proper error handling and edge case management

4

Documentation

Add explanatory comments for complex logic

Example of a well-documented function:

Copy

Ask AI

```
def filter_unknown_users(users: list[str], known_users: set[str]) -> list[str]: def  filter_unknown_users(users: list[str], known_users: set[str]) -> list[str]: """Filter out users that are not in the known users set. """Filter out users that are not in the known users set.  Args: Args: users: List of user identifiers to filter. users: List of user identifiers to filter. known_users: Set of known/valid user identifiers. known_users: Set of known/valid user identifiers.  Returns: Returns: List of users that are not in the known_users set. List of users that are not in the known_users set.  Raises: Raises: ValueError: If users list contains invalid identifiers. ValueError: If users list contains invalid identifiers.  """  """ return [user for user in users if user not in known_users]  return [user for  user in  users if  user not  in known_users]
```

## [​](#getting-help) Getting help

Our goal is to have the simplest developer setup possible. Should you experience any difficulty getting setup, please ask in the [community slack](https://www.langchain.com/join-community) or open a [forum post](https://forum.langchain.com/).

You now have everything you need to contribute high-quality documentation to LangChain! 🎤🦜

---

[Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/contributing/documentation.mdx)

[Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

[Contributing to code](/oss/python/contributing/code)