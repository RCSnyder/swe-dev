# swe-dev - Engineering Judgment for AI Coding Agents

Elevate and accelerate human thinking and judgement to help solve harder software engineering problems with rigor and legibility.

`swe-dev` is an agent plugin for VS Code Copilot, Claude Code, and GitHub Copilot CLI.

The totality of human intelligence cannot be fully reduced to a series of Markdown files, but many useful engineering habits and approaches can be made legible and reusable.

## Agents

| File                                                                                             | Purpose                                                                                                                                           |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [swe-dev-conceptual-intelligence-architect](agents/swe-dev-conceptual-intelligence-architect.md) | Turns vague ideas into concepts, analogies, systems, learning paths, opportunity theses, and testable next artifacts.                             |
| [swe-dev-visible-thinking-coach](agents/swe-dev-visible-thinking-coach.md)                       | Structures reasoning before output: clarifies the question, tests competing interpretations, exposes assumptions, and builds defensible judgment. |
| [swe-dev-verifier-first-thinking](agents/swe-dev-verifier-first-thinking.md)                     | Pressure-tests claims, analogies, and AI-written code: separates verifying from solving and replaces 'I get it' with regeneration tests.          |
| [swe-dev-high-bar-engineering](agents/swe-dev-high-bar-engineering.md)                           | Helps agents make scoped, maintainable code changes with clear plans, tests, compatibility checks, self-review, and tradeoff discipline.          |
| [swe-dev-critical-systems-engineer](agents/swe-dev-critical-systems-engineer.md)                 | Reviews critical systems for invariants, justified abstractions, failure semantics, auditability, operability, and safe change.                   |

## Layout

```text
swe-dev/
  .claude-plugin/
    plugin.json          # Plugin manifest (Claude format, cross-tool)
  agents/
    swe-dev-*.md         # Namespaced agent definitions
```

## Install

### GitHub Copilot CLI

```bash
copilot plugin marketplace add RCSnyder/swe-dev
copilot plugin install swe-dev@swe-dev
```

> The direct-URL form (`copilot plugin install https://github.com/RCSnyder/swe-dev`) still works but is deprecated.

### Claude Code

```bash
claude plugin marketplace add RCSnyder/swe-dev
claude plugin install swe-dev@swe-dev
```

### VS Code (Copilot, Preview)

Requires `chat.plugins.enabled: true`. Add the marketplace to your `settings.json`:

```json
"chat.plugins.marketplaces": [
  "RCSnyder/swe-dev"
]
```

Then run **Chat: Install Plugin** from the Command Palette and pick `swe-dev`.

VS Code also auto-discovers anything installed via the Copilot CLI from `~/.copilot/installed-plugins/`.

### Verify the install

```bash
copilot plugin marketplace list   # swe-dev should appear
copilot plugin list               # swe-dev should appear, version 1.0.0
```

Then in an interactive session:

```
/agent
```

The five `SWE Dev: ...` agents should be listed. Pick one and send a prompt to confirm it loads.

## Usage

1. Open Chat in your tool of choice.
2. Select an agent from the agent/persona picker.
3. Send a prompt, the agent's instructions, tool restrictions, and model preference apply automatically.

## Naming conventions

Everything ships under the `swe-dev-` prefix to stay collision-free as marketplaces grow.

- **Plugin name:** `swe-dev`
- **Agent files:** `agents/swe-dev-*.md`
- **Skill names / directories:** `skills/swe-dev-*/SKILL.md` (when added)
- **Slash commands:** `/swe-dev-<verb>` (when added)
- **Display `name:` in frontmatter:** `SWE Dev: <Title>` so the agent picker shows ownership at a glance

Identifier fields must be plain kebab-case — slashes or colons (`myorg/foo`) cause silent load failures in the plugin loader.

## References

- [VS Code agent plugins](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
