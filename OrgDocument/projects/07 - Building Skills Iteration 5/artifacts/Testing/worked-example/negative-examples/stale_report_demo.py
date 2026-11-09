import sys
sys.path.insert(0, "/Users/adamwang/.openclaw/workspace/organizations/ai-slowcooker/projects/01 - AI_Slowcooker/src/.github/skills/model-validatealignment/scripts")
from alignment_report import RoundState, is_stale, resolve_round_for_resume

# Scenario: BND-CHILD-SW had a round that PASSED, recorded at domain_model v1.
prior = RoundState(
    round_id="ROUND-CHILD-SW-001",
    status="PASS",
    boundary_scope_ids=["BND-CHILD-SW"],
    source_model_versions={"domain_model": "v1", "use_case_model": "v1", "ui_model": "v1"},
)

# Then someone edits the domain model (e.g. adds a new field to ServiceRequest) -> v2
current_versions_after_edit = {"domain_model": "v2", "use_case_model": "v1", "ui_model": "v1"}

print("is_stale():", is_stale(prior, current_versions_after_edit))
print("resolve_round_for_resume():", resolve_round_for_resume(prior, current_versions_after_edit))

# Compare: if nothing had changed, it should NOT be stale
current_versions_unchanged = {"domain_model": "v1", "use_case_model": "v1", "ui_model": "v1"}
print("")
print("--- counterfactual: no edit happened ---")
print("is_stale():", is_stale(prior, current_versions_unchanged))
print("resolve_round_for_resume():", resolve_round_for_resume(prior, current_versions_unchanged))
