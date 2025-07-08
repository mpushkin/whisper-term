# Investigation – Direct CLI with Clipboard

## Current Status
The application currently only supports interactive mode where users must navigate through terminal prompts to start recording. All model parameters are hardcoded (base model, English language). There's no direct CLI mode for quick transcription tasks.

## Pain Points / Opportunities
- **Power users need faster workflow**: Having to navigate interactive prompts is slow for quick transcription tasks
- **No clipboard integration**: Users must manually copy transcribed text from terminal or find saved files
- **Limited automation potential**: Current interface doesn't support scripting or integration with other tools
- **Model flexibility needed**: Users should be able to specify model via CLI args without interactive selection

## Research & Benchmarks
Based on `ai_docs/ideas/direct-cli-with-clipboard.md` research:
- **pyperclip library**: Cross-platform clipboard integration (Windows, macOS, Linux)
- **CLI argument patterns**: Standard `--record` flag pattern for direct mode
- **Existing CLI structure**: Current argparse setup can be extended with new flags
- **Minimal implementation**: Focus on `--record` flag with automatic clipboard copy

## Proposed Direction
Implement minimal direct CLI mode with:
1. `--record` flag to bypass interactive mode and start recording immediately
2. Automatic clipboard copy of transcription result
3. Enhanced CLI args for model selection (`--model`, `--language`)
4. Maintain backward compatibility with existing interactive mode
5. Simple ENTER-to-stop recording (no timeout complexity)

## Decision
**PROCEED** with minimal direct CLI implementation focusing on core workflow improvement.
Link to `design.md` for detailed solution.
