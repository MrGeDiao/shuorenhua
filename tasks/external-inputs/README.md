# External Inputs

This directory stores planning or review material that came from outside the repo's normal authoring flow.

Examples:

- ChatGPT planning packages
- Claude analysis notes
- human collaborator docs
- copied research or review prompts that shaped later work

## Rules

1. Treat each bundle as a read-only snapshot.
2. Use a dated folder name: `YYYY-MM-source-topic/`.
3. Do not mix adopted decisions into the raw source files.
4. Put repo-specific conclusions into:
   - `tasks/roadmap-*.md` for distilled plans
   - `tasks/todo-*.md` for active execution
5. If a bundle stops being useful, archive or delete it in one cleanup commit instead of letting root-level folders pile up.

## Suggested flow

1. Archive the raw input here.
2. Create a distilled roadmap that compares it to the current repo.
3. Open a versioned todo file only when implementation is ready to start.
4. Keep shipped artifacts in normal repo locations such as `references/`, `evals/`, `install/`, or `.github/`.
