# Changelog

## [1.2.0] - 2026-03-23

### Added
- Codex CLI installation guide (`install/codex.md`) with AGENTS.md, system prompt, and global instructions methods
- Codex quick start section in README

### Changed
- Moved Codex CLI content from `install/chatgpt.md` to dedicated `install/codex.md`

## [1.1.0] - 2026-03-23

### Added
- Scene-based routing: chat/status/docs/public-writing with minimal/standard/aggressive intensity levels
- Unsourced citation pattern detection (Chinese and English)
- 9 additional Chinese high-frequency AI phrases
- Misfire protection for technical system subjects
- Length-normalized thresholds for Tier 3 severity

### Changed
- Rules 3 (subject) and 5 (reader address) downgraded from hard constraints to heuristics
- Tier 1 severity: "always replace" changed to "replace by default, allow exceptions"
- Tier 3 severity: unified to length-normalized density thresholds
- Positive guidance: removed "allow tangents and half-formed thoughts", replaced with "allow casual tone without sacrificing completeness"
- Two-pass workflow now only enforced in aggressive mode

### Fixed
- Severity rules inconsistency between percentage-based and count-based thresholds
- Misfire protection now checked before Tier 1 replacement in decision flow

## [1.0.0] - 2026-03-23

### Added
- Initial release
- 10 core rules for AI writing pattern removal
- Bilingual banned phrase lists (Chinese 140+ entries, English 130+ entries)
- Chinese internet jargon coverage (赋能/闭环/抓手/etc.)
- Translation artifact detection (翻译腔)
- 13 cross-language structural anti-patterns
- 3-tier severity system with misfire protection
- 5-dimension self-evaluation scoring matrix
- Before/after examples in Chinese and English
- Two-pass workflow (rewrite + audit)
