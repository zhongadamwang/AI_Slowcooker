# Child Software Boundary — Domain Model

## Entities

### ServiceRequest *(E-002)*
**Scoped collision note**: This boundary deliberately reuses the entity ID `E-002` for a *different* concept than root-boundary's `E-002` ("ServiceRequest" as a pre-software phone/in-person request record). Here, `E-002` is the **software system's** internal `ServiceRequest` database row — created once a request is accepted into the dispatch system, with different attributes (assigned technician, scheduled time slot) than the root-level concept of the same name.

This is the fixture's deliberate scoped entity-name collision: both boundaries use entity ID `E-002` with the same display name "ServiceRequest," but they are **different entities** because their `scope` (`root-boundary` vs. `root-boundary/child-software-boundary`) differs. A validator must disambiguate by `(scope, entity_id)`, not by `entity_id` or `entity_name` alone.

### Technician *(E-003)*
A field worker assigned to a ServiceRequest within this software system.
