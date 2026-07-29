# Project Context & AI Coding Guidelines

## 1. Language Policy
- **Language**: This project exclusively uses **English** for all technical artifacts and documentation.
- This includes:
  - Source code, variables, functions, and class names.
  - Code comments and docstrings.
  - Commit messages (e.g. `feat: ...`, `fix: ...`).
  - Pull Request descriptions and GitHub Issues.
  - Markdown documentation inside the `docs/` folder (including architecture specs and step-by-step issue plans).

## 2. AI Assistant Roles & Workflow
When acting as an AI assistant (LLM) on this repository:
1. Always generate code and documentation strictly in English.
2. If reading or interacting with older Spanish documentation, naturally adopt English moving forward.
3. **Strict 1:1 Issue Mapping**: Follow a strict 1:1 mapping with GitHub Issues. Do not group multiple tasks. For each Issue `#X`, there must be exactly one corresponding specification plan (e.g. `docs/issue_x_short_name.md`).
4. **GitFlow / Trunk-based**: Never assume branches are merged to `main` by default for features. The active integration branch is `develop`. Feature branches (`feature/issue-X`) must branch from and merge back into `develop`.
