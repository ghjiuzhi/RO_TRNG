---
name: ieee-paper-writer
description: Create and maintain IEEE-style LaTeX research paper workspaces from the current repository's evidence. Use for IEEE and adjacent engineering research manuscripts when creating theme-named paper directories, LaTeX skeletons, claim-evidence tables, evidence-gap audits, related-work matrices, figure/table plans, venue-aware revision plans, or publication-ready manuscript revisions. Works with global venue profiles and project-local venue plans; all claims must be grounded in files from the current project.
---

# IEEE Paper Writer

## Core Rules

- Work inside the current project. Create or update `paper/<research_theme>/`; do not depend on another project's paper directory.
- Name paper roots by research theme, not by journal, conference, or submission round.
- Keep project-specific submission strategy in `paper/<research_theme>/venue/`.
- Keep submitted/revised packages in `paper/<research_theme>/submissions/`.
- Use global venue profiles as reusable style guidance only; do not turn every venue into a new skill.
- Do not mix reusable venue profiles with project-local venue plans.
- Use LaTeX and BibTeX for IEEE-style manuscripts unless the user asks for a different format.
- Never invent experimental results, device parameters, datasets, citations, or comparison numbers.
- Separate evidence, interpretation, limitations, and speculation.
- Preserve a claim-to-evidence trail for every abstract/conclusion-level claim.

## Workspace Layout

Create this structure when starting a new paper:

```text
paper/<research_theme>/
  AGENTS.md
  README.md
  manuscript/
    main.tex
  figures/
  refs/
    references.bib
  notes/
    project_evidence_map.md
    writing_log.md
  evidence/
    claim_evidence_table.md
    evidence_gap.md
    related_work_matrix.md
    figure_table_plan.md
  venue/
    target_venue.md
  submissions/
```

Add only files that serve the manuscript. Avoid unrelated process documentation.

## Venue Strategy

Use two layers:

- Global venue profile: reusable guidance stored with this skill, such as `references/venue_profiles/ieee_tim.md`.
- Project-local venue plan: the current manuscript's target strategy under `paper/<research_theme>/venue/`.

When adapting a manuscript to a venue:

1. Read the relevant global venue profile for general style, fit, risks, and revision priorities.
2. Read the project-local venue plan for the current target, fallback, and paper-specific framing.
3. Keep the manuscript title, claims, and evidence independent of any final submission target until the user asks for a venue-specific package.
4. Do not create a new skill for each venue.

Available draft venue profiles:

- `references/venue_profiles/ieee_tim.md`
- `references/venue_profiles/ieee_access.md`
- `references/venue_profiles/ieee_tcas2.md`
- `references/venue_profiles/ieee_tvlsi.md`
- `references/venue_profiles/jcen.md`

## Start A Paper

1. Identify the repository root and current project scope.
2. Ask for a research-theme directory name only if the user did not provide one and it cannot be inferred.
3. Create `paper/<research_theme>/` in the current project.
4. Read project-local sources first: `README*`, `AGENTS.md`, `doc/`, `data/`, `scripts/`, `rtl/`, existing manuscript notes, and generated figures/tables.
5. Build `notes/project_evidence_map.md` with local evidence paths and short notes about what each source can support.
6. Build `evidence/claim_evidence_table.md` before drafting strong claims.
7. Build or update `venue/target_venue.md` when the user asks for submission strategy.
8. Draft `manuscript/main.tex` with cautious language where evidence is incomplete.

## Evidence Discipline

For each important claim, record:

- `claim`: precise statement the paper may make.
- `evidence files`: local paths supporting it.
- `status`: established, partial, contradicted, missing, or needs replication.
- `limits`: board/device/sample/PVT/seed/toolchain boundaries.
- `paper location`: section, figure, table, or paragraph where the claim appears.

Use conservative verbs:

- Use `observed`, `measured`, `indicates`, `suggests`, `is consistent with` for bounded evidence.
- Use `demonstrates` only when the current project contains direct, repeatable support.
- Avoid certification/compliance claims unless the current project contains a complete validation package.

## Manuscript Workflow

1. Define the paper thesis in one paragraph, scoped to available evidence.
2. Draft an outline: introduction, background, design/method, experimental setup, results, discussion, limitations, conclusion.
3. Create `related_work_matrix.md` with columns for work, venue/year, method, device/domain, evidence type, limitation, and this paper's distinction.
4. Create `figure_table_plan.md` with every planned figure/table, source files, generation command if known, and manuscript message.
5. Write the abstract last, after the claim-evidence table is populated.
6. Keep limitations explicit and near the relevant result, not only at the end.
7. Ensure captions state what is measured and the experimental boundary.

## IEEE Style Preferences

- Use concise technical prose and avoid marketing language.
- Put contributions near the end of the introduction.
- Prefer numbered contributions only when they map cleanly to evidence.
- Keep related work analytical: compare assumptions, measurement scope, reproducibility, and limitations.
- Use `\cite{}` with BibTeX keys; leave `TODO-cite` markers only when a citation is genuinely missing.
- Use `figure*` and `table*` sparingly; prefer single-column floats unless width is necessary.
- Use `siunitx`, `booktabs`, `amsmath`, and `graphicx` when appropriate.

## Output Checks

Before finishing a writing pass:

- Confirm no claim depends on another project's paper directory.
- Confirm the paper root is theme-named rather than venue-named.
- Confirm venue-specific advice is either from a global profile or a local venue plan, not blurred between the two.
- Confirm every strong result claim has local evidence listed.
- Search for placeholders such as `TODO`, `TBD`, `invent`, and unresolved citation markers.
- If LaTeX tooling is available, compile the manuscript and report warnings that affect correctness.
- If compilation is not possible, state that clearly and still check file structure and cross-references.

## Global Installation Note

When turning a project-local draft into a global skill, copy this `SKILL.md` and reusable references to:

```text
~/.codex/skills/ieee-paper-writer/
```

Keep global venue profiles and reusable assets in the global skill directory. Keep project data, manuscript claims, venue plans, and submission packages inside each project's own `paper/<research_theme>/` directory.
