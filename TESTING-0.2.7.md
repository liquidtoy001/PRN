# 0.2.7 acceptance checks

Start with a fresh skill installation and an actual slide deck. Ask for notes without
configuration: the agent should show all settings together with recommendations, then wait
for one reply. Accept or modify them and verify saved preferences match the answer.

Knowledge + full + no companions must produce detailed teaching notes without generated
questions; source exercises remain explained examples. Exam + lightweight should use available
assessment evidence, with no invented probabilities. Explicit no-companion choices prevail.

Resume the same state: known preferences should not be asked again. Legacy schema-2 state
without note_configuration must validate and retain its history. PDF-only and combinations
must follow the exact deliverables list. Custom page sizes and no-deadline settings should
survive persistence. Check coverage and source visuals using the 0.2.5/0.2.6 acceptance cases.

Automated tests check CLI persistence, invalid configuration rejection and legacy compatibility;
they do not prove that every model will obey the intake or produce good teaching notes.
