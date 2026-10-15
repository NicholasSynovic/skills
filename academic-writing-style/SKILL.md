---
name: academic-writing-style
description: Reproduce the author's detailed academic voice across projects and file types while enforcing prose punctuation restrictions, acronym expansion, one sentence per source line, and strict editing scope. Apply safe corrections before collaboratively reviewing substantive changes.
---

# Academic Writing Style

## Purpose

Reproduce the author's general academic writing style across projects rather than reproducing the subject matter or organization of one manuscript.
Preserve a formal, detailed, study centered voice that explains relationships among claims, evidence, methods, contributions, and limitations.
Treat document construction and source formatting as part of the writing task rather than as separate cosmetic concerns.
Do not optimize for brevity unless the user explicitly requests it.

## Instruction authority

The user's explicit decisions govern the writing style and override conflicting examples, repository guidance, and inferred conventions, subject to the host system's governing instructions and permissions.
A later explicit user decision supersedes an earlier conflicting user decision.
Do not treat an inconsistent passage in an existing document as permission to violate a confirmed rule.
Do not infer permission to change a rule from examples alone.
If two applicable user instructions cannot be reconciled, preserve the affected content and ask a focused question before making a substantive change.

## Nonnegotiable requirements

1. Do not use colons, semicolons, or hyphens in prose anywhere in the document.
2. Place every complete prose sentence on its own source line.
3. Expand necessary acronyms at first use within every major section across all file types.
4. Consistently prefer study centered constructions and use first person only when the user explicitly requests it.
5. Preserve the author's current voice and explanatory depth unless the user explicitly requests brevity.
6. Make demonstrably low risk corrections first and then conduct the collaborative review described below.
7. Modify only the file explicitly requested by the user.
8. Do not edit figure files, table files, or research question box files under an ordinary prose editing request.

## Scope and file protection

Resolve the exact target file and its version before editing.
When multiple copies are available and the intended copy is unclear, ask which copy governs rather than silently choosing one.
Do not claim to have reviewed content that was unavailable or truncated.
Record any material coverage limitation in the review.

Permission to edit a main document does not authorize editing its dependencies.
Supporting files may be inspected when needed to understand terminology, citations, references, or construction, but inspection does not authorize modification.
Report problems in supporting files without changing them.
Do not inline an included figure, table, or question box to circumvent the file restriction.
Do not create sidecar files, reorganize directories, or update repository guidance unless separately requested.

Preserve existing citation keys, labels, cross references, input commands, paths, custom macros, and component boundaries by default.
Do not rename an identifier merely because a heading or sentence changes.
Do not add packages, replace document classes, redesign floats, change build settings, or normalize paths as part of a prose correction.
If a prose issue cannot be resolved without changing protected structure, describe the dependency and seek explicit authorization.

When a requested deliverable is a new writing file, create that file only and retain the same protections for all existing files.
Use external write tools only when the environment permits them and complete any required confirmation procedure before changing external state.
Do not describe a proposed change as an applied change.

## Prose punctuation

Treat any colon, semicolon, or hyphen in prose as a compliance error.
Apply this rule to body text, headings, titles, captions, notes, list entries, and prose inside formatting commands.
Established terminology does not receive an automatic exemption.
Do not insert a different dash character merely to evade the restriction.

Repair prohibited punctuation through grammatical rewriting rather than blind deletion.
Replace a semicolon by restructuring the relationship or using separate complete sentences.
Replace a colon by integrating the explanation into the sentence or expressing it in a following sentence.
Rewrite a hyphenated construction using an accurate form without a hyphen.
Do not change a technical meaning or introduce a nonstandard technical expansion without review.

Distinguish prose from structural and literal content.
Protect command names, citation keys, labels, file paths, URLs, code, configuration syntax, mathematical operators, and machine interpreted identifiers.
A colon inside a label is structural rather than narrative punctuation.
Prose arguments of a command remain prose even though they are inside LaTeX syntax.

Do not silently alter an exact quotation, a published title, a reported instrument item, or a literal identifier to make it appear compliant.
Flag the conflict and propose an appropriate alternative such as paraphrasing when the intended meaning can be retained.
If a prohibited mark remains in prose because the issue requires a user decision, report the unresolved error.
Do not claim that the document passes the punctuation check while such errors remain.

## Sentence oriented source formatting

Place each complete prose sentence on exactly one physical source line.
Do not wrap a sentence at an arbitrary character count.
Do not place multiple sentences on the same source line.
Separate paragraphs with a blank line without turning each sentence into its own paragraph.
Keep a sentence's citation and associated inline commands on the same line as the sentence.

Recognize abbreviations, decimal values, citation keys, commands, and other nonsentence periods before splitting lines.
Do not use a period followed by a space as the sole sentence segmentation rule.
Preserve indentation and environment structure where they are meaningful.
Structural commands, metadata, code, and mathematics follow their own syntax rather than being forced into prose sentence segmentation.
Apply the sentence rule to any editable prose inside headings, captions, notes, or other containers without breaking their syntax.

When the source format does not expose physical text lines, preserve sentence boundaries through the format's supported editing representation and state any limitation.
Do not insert visible paragraph breaks or forced layout breaks merely to simulate source line boundaries.

## Acronyms across file types

At first use within each major section, write the full term followed by the acronym in parentheses.
Use the acronym thereafter within that section when it aids clarity.
Repeat the expansion at first use in each subsequent major section.
Do not repeatedly expand an acronym within the same major section without a specific reason.

Use the file's existing major structural divisions.
In LaTeX, use each section as the expansion boundary.
In other formats, use the equivalent major division without imposing an arbitrary new hierarchy.
For an unsectioned document, expand the acronym at first use in the document.
Apply the rule to prose regardless of file extension.

Use an established expansion supported by the document or available evidence.
Do not invent an expansion, reinterpret a proper name as an acronym without justification, or silently change technical terminology.
Ensure that expansions also obey the punctuation prohibition.
If an acronym is introduced only in a protected included component, do not assume that this licenses unexplained use in the editable prose.
Expand it appropriately in the requested file or flag a conflict when that cannot be done safely.

## Voice and grammatical subjects

Consistently prefer study centered constructions unless the user explicitly requests first person.
Name the study, analysis, procedure, evidence, participants, records, or contribution as the grammatical subject when appropriate.
Prefer a clear actor and action rather than automatically converting sentences into passive voice.

Existing first person wording does not itself authorize continued first person writing.
Rewrite first person narration when the responsible actor and meaning are unambiguous.
Flag cases where replacement could misattribute a completed contribution, decision, or responsibility.
Do not rewrite participant quotations or other exact evidence merely to remove first person.
Keep those conflicts visible for review.

Preserve formal terminology and controlled distinctions.
Do not replace a precise term with a looser synonym solely to avoid repetition.
Avoid promotional language, unsupported novelty claims, and claims of universal relevance that exceed the evidence.

## Depth and explanatory completeness

Do not shorten prose by default.
Preserve meaningful context, methodological detail, qualifications, and connections among ideas.
Do not impose arbitrary sentence length or paragraph length targets.
Improve clarity by making relationships explicit rather than by systematically compressing the text.

Retain complexity when it carries necessary meaning.
Split or restructure a sentence when needed for grammar, flow, or accurate interpretation, not merely because the sentence is long.
Do not expand prose with empty repetition or unsupported background.
Distinguish deliberate reinforcement of an important boundary from accidental duplication.

## Evidence and claim discipline

Identify the kind of evidence supporting a claim before selecting its verb and strength.
Keep observations, documented descriptions, participant accounts, analytical interpretations, and proposed procedures distinct.
Do not describe reported behavior as independently verified behavior.
Do not treat instructions as proof of execution or successful execution as proof of appropriateness.

Attach a limitation to the specific inference it constrains.
Explain whether the limitation concerns classification, temporal ordering, comparison, causal interpretation, generalization, or another identifiable issue.
Avoid adding generic caveats that do not change interpretation.
Preserve missing, unresolved, and insufficient evidence as explicit states rather than silently assigning them to an opposing category.

Use present tense for current arguments and established descriptions, past tense for completed actions and findings, and future or conditional language for proposed work as appropriate.
Never make planned work sound completed.
Separate required work, necessary support, and optional extensions when those categories apply.
Do not weaken every required procedure into a possibility or convert every optional application into a commitment.

Do not import the preliminary exam's research topics, study count, populations, methods, or specific limitations into unrelated projects.
Transfer the reasoning discipline rather than the original research design.

## Paragraphs and document flow

Give each paragraph a coherent analytical purpose.
Common purposes include establishing a problem, synthesizing evidence, defining a gap, explaining a procedure, interpreting an implication, and delimiting a conclusion.
Do not force all sections into one rigid paragraph template.

Build transitions by explaining why the next idea follows from the preceding one.
Distinguish motivation, prior knowledge, completed contributions, proposed work, operational detail, and interpretation.
Use the document's existing hierarchy and references to keep these functions connected without reproducing all details in every section.

Preserve meaningful relationships across sections.
When the same boundary appears repeatedly, assess whether each occurrence performs a different explanatory role.
Do not remove substantive repetition merely to make the document shorter.
Flag major reordering, paragraph consolidation, or changes to argumentative emphasis for discussion before applying them.

## Citations and references

Preserve existing citation and reference identifiers unless the user authorizes a change.
Keep citations attached to the propositions they support.
Do not infer a source's contents from its title or citation key.
Do not invent citations, results, counts, quotations, or bibliographic details.

Consider existing bibliography entries before proposing additional literature.
Reuse an entry only when its actual contents support the claim.
Flag unsupported assertions and describe the evidence needed rather than attaching a convenient but unrelated citation.
Treat literature discovery as a separate research action when additional evidence is needed.

## Document construction

Preserve the separation between narrative prose and reusable presentation components.
Keep included figures, tables, and question boxes in their existing files.
Use the requested document to introduce, reference, and interpret those components without taking ownership of their implementation.

Respect local macros and established cross reference conventions.
Do not infer build correctness from the presence of a command or package.
Report suspected path problems, missing definitions, or component inconsistencies separately from prose findings.
Do not perform structural repairs without authorization.

## Editing sequence

### Establish the target and constraints

Identify the requested file, task, available version, and explicit user overrides.
Read enough context to understand the passage's role and preserve its dependencies.
Determine whether the task permits editing or only review.
For a review only request, describe proposed corrections without modifying the file.
For an editing request, proceed with the low risk pass before substantive review.

### Apply low risk corrections

Correct obvious spelling errors, unambiguous grammatical errors, sentence line formatting, and prohibited punctuation when the repair clearly preserves meaning.
Normalize paragraph separation where the intended boundaries are unambiguous.
A correction is low risk only when it does not change a claim, technical definition, evidentiary status, citation relationship, methodological commitment, or structural dependency.

Remove an adjacent exact duplicate only when it is clearly accidental and removal preserves every meaningful citation and structural element.
Otherwise, flag duplication for review.
Do not invent missing wording, resolve an ambiguous fragment by guessing, or rewrite uncertain technical terminology during this pass.
If no safe correction is available, leave the passage unchanged and explain why.

### Review substantive issues

Review document construction, organization, argument, paragraph flow, sentence relationships, terminology, evidence, and claim boundaries.
Separate confirmed errors from stylistic preferences and unresolved questions.
For each material issue, identify the location, explain its consequence, and propose a solution.
Identify changes that would require editing a protected dependency without performing them.

### Ask focused questions and iterate

Ask only questions whose answers could materially change the revision.
Do not ask the user to reconfirm decisions already established.
Resolve uncertainties about meaning, evidence, commitments, emphasis, or structure before drafting substantive changes.
After the user resolves the relevant issues, revise within the authorized scope.
Retain all decisions that continue to apply.

### Validate and report

Review the resulting diff or equivalent change record.
Confirm that only the requested file was modified.
Check that protected identifiers and inclusion boundaries remain intact.
Check prohibited punctuation in prose using context aware inspection rather than a raw whole file character ban.
Check sentence line boundaries, acronym expansion within each major section, first person narration, and preservation of substantive detail.

Check that low risk corrections have not introduced fragments, comma splices, changed citation scope, or altered technical meaning.
Report applied changes separately from proposed changes and unresolved issues.
Do not claim successful compilation, complete review, or full compliance unless the corresponding check was actually performed and supported.

## Default review response

Report safe corrections already applied, or state that none were applied.
Then present substantive findings grouped by construction, organization, and prose as appropriate.
Explain proposed solutions and conclude with focused questions only when decisions remain unresolved.
Do not append a generic invitation to continue.
Do not reproduce the entire document when a scoped report or diff is sufficient, unless the user requests the complete revised text.

## Completion criteria

The requested work is complete only when the authorized edits are present, the applicable checks have been performed, and unresolved conflicts are explicitly reported.
A document with known remaining prose violations must not be described as fully compliant.
A proposal must not be described as an edit, a read must not be described as a persistent import, and an unperformed build must not be described as a successful validation.
