# Mosaic Agent-Friendly Representation Design

## Purpose

Build an agent-friendly representation layer for Mosaic that lets LLM/LVLM-style agents reason over 3DGS SLAM outputs without consuming raw Gaussian splats, point clouds, or dense map dumps directly.

The layer should turn Mosaic's metric 3D substrate into bounded, typed, evidence-carrying query results for perception, navigation, coordination, belief inspection, and eventual embodied tool orchestration.

This spec merges two inputs:

1. The Argus layered belief graph design for general-purpose indoor/outdoor robot swarms.
2. The ARNA paper notes showing that strong navigation agents rely on coordinated memory and tools: textual memory, raster/top-down spatial memory, scene-graph landmarks, reasoning tools, and navigation/control primitives.

## Chosen Approach

Use a **Layered Belief Graph + Agent Tool Memory** architecture.

This is the Argus design extended with the ARNA lesson: the agent should not reason from one monolithic world model. It should use synchronized memory views and typed tools:

- A grounded 3D substrate from Mosaic splat maps and poses.
- A metric/raster memory for occupancy, explored space, frontiers, and traversability.
- A topology/scene graph memory for regions, landmarks, objects, hazards, and relations.
- A textual summary memory for compact agent context.
- A belief/provenance model for confidence, source, timestamp, evidence, staleness, and conflicts.
- A commitment model for tasks, reservations, route/resource locks, and swarm intentions.
- A deterministic query/tool API over those memories.

The first implementation should be a typed Python library layer, not an LLM provider integration, ROS node, Habitat runner, or full ARNA reproduction.

## Architecture

```text
Mosaic 3D substrate
  Gaussian splats, SplatMap snapshots, frames, poses, camera observations
        ↓
Metric / raster memory
  occupancy cells, explored cells, frontier candidates, traversability hints
        ↓
Region + topology memory
  regions, paths, adjacency, rooms/zones, terrain patches, route segments
        ↓
Semantic scene graph memory
  objects, hazards, humans, landmarks, affordances, spatial relations
        ↓
Belief + provenance memory
  claims, confidence, source, observed_at, evidence refs, conflicts, staleness
        ↓
Textual summary memory
  compact region summaries, search notes, failed attempts, uncertainty notes
        ↓
Commitment memory
  task assignments, route reservations, resource locks, robot intentions
        ↓
Agent-facing tools
  perceive, reason, navigate, coordinate, inspect belief, retrieve evidence
```

The dense 3D representation remains the grounded evidence layer. Agents consume compact tool results that include provenance and uncertainty.

## ARNA-Informed Design Principles

ARNA's reported gains come from orchestrating tools and memory, not from exposing raw 3D geometry to the LVLM. Mosaic should adopt that pattern while staying backend-agnostic.

### 1. Separate memory views

Mosaic should expose synchronized but distinct memory views:

- **Spatial/raster memory:** grid-like explored/free/occupied/frontier/traversability state.
- **Scene graph memory:** landmarks, objects, hazards, rooms/zones, and relations.
- **Text memory:** concise summaries and search history suitable for prompt context.
- **Belief memory:** claim status, confidence, source, evidence, stale/conflicted state.
- **Commitment memory:** team-level task and resource commitments.

This mirrors ARNA's textual memory, raster/top-down memory, and scene-graph landmarks, but generalizes them for indoor/outdoor swarms and non-Habitat backends.

### 2. Tool-first agent interface

Agents should call deterministic Mosaic tools instead of inspecting full state. Initial tool families:

- Perception/search tools.
- Navigation/reasoning tools.
- Coordination/commitment tools.
- Belief/provenance tools.
- Memory/context tools.

Tool outputs must be schema-valid, bounded, and deterministic for a fixed world state.

### 3. Claims, not truth

Observations become claims with evidence. Conflicts remain visible rather than being silently merged away.

### 4. Evaluation through ablations

ARNA's ablations show that removing scene graph, occupancy/raster memory, or reasoning programs can collapse performance. Mosaic should include small synthetic ablations:

- No scene graph memory.
- No raster/frontier memory.
- No belief/provenance metadata.
- Tool-free summary-only access.

The first tests should verify that these removals degrade or block specific capabilities in deterministic scenarios.

## Core Data Model

### Identifiers

All public representation entities should use typed string identifiers:

```text
RobotId
RegionId
EntityId
ClaimId
CommitmentId
EvidenceRef
```

These can be lightweight value dataclasses in the first implementation.

### Entity Kinds

The first implementation should support:

- `robot`
- `region`
- `frontier`
- `path_segment`
- `terrain_patch`
- `object`
- `hazard`
- `human`
- `landmark`
- `affordance`
- `task`
- `resource`
- `commitment`

### Relation Kinds

The first implementation should support:

- `contains`
- `connects`
- `near`
- `blocks`
- `observed_by`
- `reachable_by`
- `assigned_to`
- `reserved_by`
- `requires_capability`
- `has_affordance`
- `conflicts_with`

### Claim Model

The key primitive is a **claim with evidence**:

```yaml
id: claim_123
subject: path_segment_4
predicate: blocked_by
object: hazard_12
confidence: 0.74
source:
  type: robot
  id: rover_3
observed_at: 2026-05-18T10:41:00Z
frame_id: map
valid_until: 2026-05-18T10:46:00Z
evidence:
  type: splat_region
  uri: mosaic://splat-map/session_22/region_91
conflicts_with:
  - claim_098
status: active
```

`source` may be a robot, detector, planner, human operator, simulator, imported map, or offline evaluator.

### Claim Statuses

- `active`: currently accepted as best available belief.
- `superseded`: replaced by newer or better evidence.
- `conflicted`: contradicted by another live claim.
- `stale`: no longer fresh enough for confident action.
- `rejected`: failed validation or known false positive.

### Evidence References

Evidence references should be opaque strings plus a type field. Initial evidence kinds:

- `splat_map`
- `splat_region`
- `camera_frame`
- `image_region`
- `raster_cell`
- `detector_output`
- `human_note`
- `simulator_state`

The representation layer should not load the evidence payload unless a caller explicitly asks to retrieve it.

## Memory Models

### Spatial / Raster Memory

Purpose: ARNA-like top-down spatial memory generalized for Mosaic.

Minimum state:

- frame id
- resolution
- cell coordinates
- occupancy state: `unknown`, `free`, `occupied`
- explored flag
- frontier flag
- optional traversability score by robot type
- optional evidence claim IDs

Initial tools over this memory:

```text
get_frontiers(region=None, robot_type=None)
query_traversability(region_or_path, robot_type)
summarize_spatial_memory(region=None)
```

### Scene Graph Memory

Purpose: semantic/topological state for agent reasoning.

Minimum state:

- nodes for entities and regions
- relations with confidence and claim references
- object/hazard/landmark labels
- region containment and adjacency
- evidence references

Initial tools:

```text
find_objects(query, region=None, min_confidence=None)
find_hazards(region=None, hazard_type=None)
query_scene_graph(subject=None, predicate=None, object=None)
summarize_region(region_id, include_uncertainty=True)
```

### Textual Memory

Purpose: compact prompt-ready summaries without forcing the agent to infer from full graph state.

Minimum state:

- region summaries
- search notes
- failed attempts
- uncertainty warnings
- last-updated timestamp
- source claim IDs

Initial tools:

```text
remember_note(scope, text, source_claims=())
summarize_context(region=None, task=None, max_items=10)
list_uncertainty_notes(region=None)
```

### Belief Memory

Purpose: confidence, conflicts, staleness, provenance, and evidence traceability.

Initial tools:

```text
get_confidence(claim_or_entity_id)
check_staleness(claim_or_region_id)
compare_claims(claim_ids)
retrieve_evidence(claim_id)
request_confirmation(target, preferred_robot_type=None)
```

### Commitment Memory

Purpose: multi-robot coordination and conflict prevention.

Initial tools:

```text
allocate_task(task, candidate_robots=None)
reserve_resource(resource_id, robot_id, time_window)
list_commitments(region=None, robot_id=None)
detect_conflicts(plan_or_commitment)
```

## Agent Query API

The agent API should be deterministic and local. It should return typed Python objects that can later be serialized as tool-call JSON.

### Perception/Search

```text
find_objects(query, region=None, min_confidence=None)
find_hazards(region=None, hazard_type=None)
summarize_region(region_id, include_uncertainty=True)
retrieve_evidence(claim_id)
```

Expected result shape:

```yaml
objects:
  - id: object_42
    label: red_vehicle
    region: region_8
    confidence: 0.81
    source:
      type: robot
      id: drone_2
    observed_at: 2026-05-18T10:40:12Z
    evidence: image://drone_2/frame_5401
```

### Navigation/Reasoning

```text
get_frontiers(region=None, robot_type=None)
query_traversability(region_or_path, robot_type)
plan_route(robot_id, goal, constraints=None)
explain_blockage(route_or_region)
```

Expected result shape:

```yaml
feasible: false
reason: path_segment_4 blocked_by hazard_12
confidence: 0.74
source:
  type: robot
  id: rover_3
alternatives:
  - send_robot: legged_1
  - request_confirmation: drone_2
  - route: path_segment_7
```

### Coordination

```text
allocate_task(task, candidate_robots=None)
reserve_resource(resource_id, robot_id, time_window)
list_commitments(region=None, robot_id=None)
detect_conflicts(plan_or_commitment)
```

Expected result shape:

```yaml
selected_robot: legged_1
reason: highest feasibility under terrain and battery constraints
commitments_created:
  - commitment_22
conflicts:
  - resource corridor_4 reserved by rover_2 until 10:47
```

### Belief/Provenance

```text
get_confidence(claim_or_entity_id)
check_staleness(claim_or_region_id)
compare_claims(claim_ids)
request_confirmation(target, preferred_robot_type=None)
```

Expected result shape:

```yaml
claim: claim_123
status: stale
reason: valid_until elapsed
recommended_action:
  request_confirmation:
    target: path_segment_4
    preferred_robot_type: drone
```

### Memory/Context

```text
remember_note(scope, text, source_claims=())
summarize_context(region=None, task=None, max_items=10)
list_uncertainty_notes(region=None)
```

Expected result shape:

```yaml
summary:
  region: region_8
  notes:
    - text: rover_3 reported corridor_4 blocked, but drone_2 has not confirmed it
      source_claims: [claim_123]
      uncertainty: conflicted
```

## Observation-to-Belief Flow

```text
Mosaic observation or splat-map update
  camera observations, poses, SplatMap snapshots, posterior query results
        ↓
Local extractors
  occupancy/raster cells, frontiers, objects, hazards, traversability hints
        ↓
Claim builder
  entity IDs, relation IDs, confidence, timestamp, source, evidence reference
        ↓
Belief update
  insert, supersede, mark conflict, mark stale, reject invalid claims
        ↓
Memory projection
  update raster memory, scene graph memory, textual summaries, commitments
```

The first implementation can use synthetic extractor outputs. It does not need object detection, segmentation, or real splat-to-occupancy conversion.

## Agent-Decision-to-Action Flow

```text
Agent calls Mosaic tool
  find, summarize, route, inspect, allocate, reserve
        ↓
Representation service checks memory
  scene graph, raster memory, belief status, commitments
        ↓
Tool returns bounded recommendation
  confidence, evidence, conflicts, alternatives, missing info
        ↓
External executor decides action
  goto, rotate, follow path, explore frontier, request confirmation
        ↓
Execution feedback becomes claims
  completed, failed, blocked, newly observed, contradiction
```

Mosaic should expose action recommendations and commitment records, not directly command robots in the first implementation.

## Testing Strategy

### Unit Tests

- Identifier validation.
- Claim creation and required metadata validation.
- Claim status transitions.
- Entity/relation insertion.
- Frozen query result mappings.
- Spatial memory cell validation.
- Scene graph relation queries.
- Text memory bounded summaries.
- Commitment conflict detection.

### Integration Tests

- Synthetic observations create entities, relations, and claims.
- Conflicting robot reports stay visible.
- Stale claims trigger confirmation recommendations.
- Blocked path claims cause route degradation.
- Frontier queries use raster memory.
- Object/hazard queries use scene graph memory.
- Context summaries cite source claims.
- Task allocation respects robot capabilities and commitments.

### Scenario Tests

1. **Indoor blocked doorway:** wheeled robot reroutes; drone is recommended for confirmation.
2. **Outdoor rough terrain:** legged robot is preferred over wheeled robot.
3. **Search frontier conflict:** two robots disagree about traversability and the query returns uncertainty.
4. **Manipulation precondition:** object exists but no available robot has the required affordance.
5. **ARNA-style memory ablation:** scene graph or raster memory removal prevents the corresponding query from returning a confident answer.

## Non-Goals

- Do not reproduce ARNA's full Habitat/GPT-4o evaluation loop in Mosaic's first implementation.
- Do not integrate an LLM/LVLM provider.
- Do not require robot hardware or ROS.
- Do not implement real object detection, room segmentation, or Grounding DINO integration.
- Do not make agents consume raw splats, point clouds, or full graph dumps.
- Do not solve low-level SLAM or Gaussian optimization in this layer.
- Do not assume a single perfectly consistent global map in swarm settings.

## Open Design Constraints

These should be made concrete in the implementation plan:

1. Start with in-memory dataclass stores; defer database storage.
2. Start with Python library APIs; defer network service/ROS wrappers.
3. Use opaque evidence URIs; defer evidence payload retrieval.
4. Store commitments in the same in-memory world model initially; split later only if needed.
5. Keep IDs caller-supplied for deterministic tests; defer automatic entity resolution.

## Success Criteria

Minimum successful demo:

1. Ingest synthetic observations from at least two robots.
2. Create entities, relations, claims, raster cells, text notes, and commitments with provenance.
3. Detect a conflict between two robot observations.
4. Answer one query from each tool family.
5. Return route or task recommendations with confidence, evidence, and explanation.
6. Degrade recommendations when required data is stale, conflicted, or unavailable.
7. Demonstrate ARNA-style memory separation by testing scene graph and raster memory independently.
