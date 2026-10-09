# Dream — Project Rules

- Dream is a lightweight GitHub development plugin for ChatGPT. Keep its implementation simple and maintainable.
- Use English for code, comments, documentation, commits, Issues, and Pull Requests.
- Follow the existing project structure and naming conventions.
- Prefer small, focused changes. Avoid unnecessary abstractions, files, and dependencies.
- Reuse existing functionality before introducing new solutions.
- Keep `plugin.json` and `.codex-plugin/plugin.json` consistent, including their versions.
- Keep bundled Ponytail and Grill Me skills intact unless an update is explicitly required.
- Maintain compatibility with the supported ChatGPT plugin format.
- Never commit secrets, credentials, generated archives, or temporary files.
- Run `python3 scripts/validate_plugin.py` and verify GitHub Actions checks before merging changes.
- Update `README.md` when user-facing functionality or installation requirements change.
- Keep the repository clean and avoid unrelated changes.
