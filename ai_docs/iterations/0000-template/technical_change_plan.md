<!-- TEMPLATE ONLY – COPY THIS FILE TO START A NEW ITERATION -->
# Technical Change Plan – <iteration title>

## Summary
Briefly restate the goal in one or two sentences and link back to `design.md`.

## Code Changes (by module / file)
| Path | Change Type | Description |
|------|-------------|-------------|
| src/module/foo.py | new | Add `FooBar` class implementing … |
| src/utils/id.py   | modify | Refactor `generate_id` to return UUID4 |

## Data & Schema Changes
Describe any DB migrations, new tables, config files, or data formats.

## API / Interface Changes
List new endpoints, CLI flags, public functions, or breaking changes.

## Dependencies & Configuration
New third-party libs, env vars, feature flags, or build steps.

## Detailed Steps
1. Step-by-step technical sequence (e.g. add unit tests, implement FooBar, update docs).
2. …

## Testing Strategy
- Unit tests to add/adjust (paths, edge-cases)
- Integration tests (components, fixtures)
- Manual verification steps (if any)

## Rollback / Migration Plan
How to revert if deploy fails and how to migrate data safely.

## Risks & Mitigations (technical only)
Identify potential technical pitfalls and countermeasures.
