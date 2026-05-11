---
name: requirements-sanitize
description: Sanitize raw requirements documents before ingestion by removing or reclassifying non-business content. Filters out IT infrastructure details, software implementation specifics, and operational procedures that obscure business intent. Outputs a clean, business-focused requirements document ready for requirements-ingest. Use when the source document mixes business requirements with technical/operational/infrastructure perspectives and needs to be cleaned up first.
license: MIT
---

# Requirements Sanitize

## Intent

Pre-process raw requirements documents by removing noise from non-business perspectives (IT infrastructure, software implementation, operational procedures) and surfacing the underlying business process intent. Produces a clean, business-focused document suitable as input to `requirements-ingest`.

Raw documents often arrive as conversation transcripts, IT change requests, operational runbooks, or software design notes. These contain implementation decisions masquerading as requirements. This skill strips that noise so downstream skills reason about *what the business needs*, not *how a previous team chose to build it*.

## Inputs

- **Raw document**: Any text-based source — conversation transcript, email thread, operational procedure, IT change request, software spec, or informal description
- **Target domain** *(optional)*: The business domain or system under analysis (e.g., "customer onboarding", "order management"); helps the skill anchor business-relevant content
- **Sanitization mode** *(optional)*: `strict` (remove all non-business content) | `annotate` (keep non-business content but tag it) | `transform` (rewrite non-business statements as business intents). Default: `transform`

## Outputs

- **Sanitized requirements document** (`sanitized-requirements.md`) — Business-focused requirements with non-business content removed or rewritten
- **Sanitization report** (`sanitization-report.md`) — Summary of changes: items removed, items transformed, items retained as-is, and rationale

## Perspective Classification

The skill classifies each statement in the source document by perspective before deciding how to handle it:

| Perspective | Examples | Default Action |
|-------------|----------|----------------|
| **Business process** | "Customer submits an order", "Manager approves the request", "System notifies the user" | Retain as-is |
| **Business rule** | "Orders above $10,000 require dual approval", "Returns are accepted within 30 days" | Retain as-is |
| **User goal / outcome** | "Sales team needs to track pipeline by region", "Users should be able to self-serve" | Retain as-is |
| **Operational procedure** | "Operator clicks Export, saves CSV, emails to Finance" | Transform → business intent |
| **IT infrastructure** | "Deploy on AWS EKS, 3 replicas, behind an ALB", "PostgreSQL 14 on RDS" | Remove (flag if it implies a constraint) |
| **Software implementation** | "Use REST API with JWT auth", "React frontend with Redux state management" | Remove (flag if it implies a capability need) |
| **Organisational / team structure** | "The DevOps team will maintain the pipeline" | Remove unless it identifies a business actor |
| **Ambiguous / mixed** | Statements that blend business intent with implementation detail | Transform → extract business intent |

## Workflow

### Step 1 — Parse and segment the document

Split the raw document into discrete statements. Each statement is the smallest unit that carries a single idea (sentence, bullet point, or numbered item).

### Step 2 — Classify each statement by perspective

Apply the Perspective Classification table above to every statement. Mark each with one of:
- `RETAIN` — pure business content
- `TRANSFORM` — contains business intent but wrapped in implementation language
- `REMOVE` — purely technical/operational/infrastructure with no business dimension
- `FLAG` — ambiguous; needs human review

### Step 3 — Apply sanitization actions

**For `TRANSFORM` statements**: Rewrite to express the underlying business intent.

Examples:
- *Before*: "The batch job runs nightly at 2 AM via cron to generate reconciliation files."
  *After*: "The system shall perform daily financial reconciliation."
- *Before*: "We'll use SendGrid to send password reset emails."
  *After*: "The system shall support user-initiated password reset via email notification."
- *Before*: "The API endpoint POST /orders will accept JSON payloads validated against the OpenAPI schema."
  *After*: "Users shall be able to submit new orders to the system."

**For `REMOVE` statements**: Discard but log in the sanitization report.

**For `FLAG` statements**: In `annotate` mode, keep with a `[REVIEW NEEDED]` tag. In `transform` mode, attempt a best-effort rewrite and mark as `[TRANSFORMED — review recommended]`. In `strict` mode, remove.

### Step 4 — Reconstruct the sanitized document

Regroup retained and transformed statements into logical sections matching a standard business requirements structure:

1. **Business Context** — Purpose, background, and scope
2. **Actors and Stakeholders** — Who is involved (business roles, not technical teams)
3. **Business Processes** — What must happen (process flows, activities, decisions)
4. **Business Rules** — Constraints and conditions governing the process
5. **System Capabilities** — What the target system must do to support the business (functional)
6. **Quality and Compliance Expectations** — Non-functional expectations expressed in business terms (SLAs, regulatory obligations)
7. **Out of Scope** — Explicitly excluded items, if mentioned

Omit sections for which no content exists.

### Step 5 — Generate the sanitization report

Produce a concise report listing:
- Count of statements retained, transformed, removed, and flagged
- Per-statement log for `TRANSFORM` and `REMOVE` decisions (original → outcome + rationale)
- Recommended follow-up actions (e.g., "Validate transformed statements with business stakeholder")

### Step 6 — Output files

Write both output files to the project artifacts directory:
- `outputs/projects/{project_id}/Requirements/sanitized-requirements.md`
- `outputs/projects/{project_id}/Requirements/sanitization-report.md`

If `project_id` is unknown, output inline and advise the user to save before proceeding.

## Sanitization Heuristics

Use these signals to identify non-business content:

**Technology indicators** (likely `REMOVE` or `TRANSFORM`):
- Cloud provider names (AWS, Azure, GCP) and service names (EC2, S3, Kubernetes)
- Database products and versions (PostgreSQL, MySQL, MongoDB, Oracle)
- Programming languages, frameworks, or libraries
- Network topology terms (VPN, subnet, load balancer, CDN)
- CI/CD and DevOps terminology (pipeline, container, Dockerfile, Terraform)
- API design vocabulary (endpoint, REST, GraphQL, JSON, XML schema)
- Authentication protocols used as implementation choices (JWT, OAuth2, SAML as tech choices vs. business access-control requirements)

**Operational indicators** (likely `TRANSFORM`):
- Named actors performing manual steps that could be system-automated
- Step-by-step procedures describing *how* rather than *what* or *why*
- References to specific tools used by operators (e.g., "uses Excel to…", "logs into the admin console and…")
- Scheduling/timing expressed in infrastructure terms (cron, batch window, scheduled task)

**Business content signals** (likely `RETAIN`):
- Subject is a business role (Customer, Manager, Finance Team, Approver)
- Verb expresses a business outcome (submit, approve, notify, generate, review, reject)
- Sentence can be validated by a business stakeholder without technical knowledge
- Contains a business rule condition (if/when + business event → business outcome)

## Integration

**Upstream**: None — this skill is the first step in the pipeline when source documents are unclean.

**Downstream**: `requirements-ingest` — pass `sanitized-requirements.md` as the input document.

**Typical pipeline**:
```
[Raw document] → requirements-sanitize → sanitized-requirements.md
                                       ↓
                              requirements-ingest → requirements.md / requirements.json
                                       ↓
                              goals-extract, process-w5h, domain-extractconcepts …
```

## Example Prompt

```
Use the requirements-sanitize skill to clean this document before ingestion.
Target domain: Customer Order Management
Sanitization mode: transform

[PASTE RAW DOCUMENT HERE]

Project ID: ORDER-MGMT-001
```

## Quality Checks

Before handing off to `requirements-ingest`, verify:
- [ ] Every retained statement is understandable by a non-technical business stakeholder
- [ ] No implementation technology names remain in the sanitized document (unless they are a business constraint, e.g., "must integrate with SAP")
- [ ] All business actors are expressed as roles, not team names or job titles tied to a specific org chart
- [ ] Transformed statements preserve the original intent — none have changed *what* the business needs
- [ ] `FLAG` items have been reviewed and resolved
