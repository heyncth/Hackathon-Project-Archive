# Engineering Case Study Template

<!--
Hand-authored research product. Never auto-generated.
Publish only when docs/verification-policy.md case-study gate passes.
Distinguish FACT (with evidence link) from ANALYSIS/INFERENCE explicitly.
Never invent architectural details.
-->

# {{ project.name }} — Engineering Case Study

## Problem and constraints

<!-- What problem did the team face at the hackathon? Time, team size,
     hardware, data constraints. Cite sources; mark unknowns. -->

## Available evidence and source limitations

<!-- List what was read (repos, write-ups, talks) and what is missing. -->

## System architecture

<!-- FACTS only where evidenced. Use "INFERENCE:" prefix for analysis. -->

## Verified technical decisions

<!-- Each decision: what, why (if evidenced), source link. -->

## Trade-offs and limitations

## Engineering lessons

<!-- Clearly labeled analysis, not fact. -->

## Facts versus analysis

<!-- One-paragraph summary of which claims above are fact vs inference. -->

## References

{{ for evidence in evidence_list }}
- {{ evidence.claim }} — {{ evidence.url }}
{{ endfor }}
