# %% [markdown]
# # Mosaic full-power demo
#
# This script is written like a Jupyter notebook export.
# Each `# %%` block can be run as a cell in editors such as VS Code,
# JupyterLab with jupytext-style tooling, or plain Python.

# %% [markdown]
# ## Cell 1 — Import Mosaic
#
# Mosaic is a typed Python library for robot perception maps.
# It provides small contracts for camera data, SLAM backends, splat maps,
# map fusion, evaluation, and agent-friendly map queries.

# %%
from pathlib import Path
from pprint import pprint

import mosaic

print("Mosaic version:", mosaic.__version__)
print("Number of public API exports:", len(mosaic.__all__))
print("Some public APIs:")
pprint(mosaic.__all__[:20])

# %% [markdown]
# ## Cell 2 — See built-in robot camera rigs
#
# A camera rig describes where cameras are mounted on a robot.
# Mosaic includes a few built-in examples.

# %%
from mosaic.platforms import default_platform_registry

registry = default_platform_registry()

print("Built-in platforms:", registry.names)

for name in registry.names:
    platform = registry.get(name)
    print()
    print("Platform:", platform.name)
    print("Robot type:", platform.embodiment.value)
    print("Base frame:", platform.base_frame.value)
    print("Cameras:", platform.camera_rig.camera_ids)

# %% [markdown]
# ## Cell 3 — Make a fake camera sequence
#
# A sequence is a stream of camera observations.
# This synthetic one is tiny and deterministic, which makes it useful for demos and tests.

# %%
from mosaic.evaluation import synthetic_forward_sequence

scenario = synthetic_forward_sequence(frame_count=5)

print("Scenario name:", scenario.name)
print("Number of frames:", len(scenario.sequence))
print("Camera IDs in first frame:", scenario.sequence.observations[0].camera_ids)

first_observation = scenario.sequence.observations[0]
print("First timestamp:", first_observation.timestamp.nanoseconds, "nanoseconds")
print("First camera pose:", first_observation.views[0].camera_pose)

# %% [markdown]
# ## Cell 4 — Run the deterministic SLAM backend
#
# SLAM means "simultaneous localization and mapping."
# The included backend is intentionally fake and deterministic.
# It creates one splat for each camera frame so the whole pipeline can be tested.

# %%
from mosaic.core import FrameId
from mosaic.slam import DeterministicSplatBackend

backend = DeterministicSplatBackend(map_frame=FrameId("map"))
updates = []

for observation in scenario.sequence:
    update = backend.process(observation)
    updates.append(update)
    print(
        "time:",
        observation.timestamp.nanoseconds,
        "| tracking:",
        update.tracking_state.value,
        "| new splats:",
        len(update.map_update),
        "| total splats:",
        update.diagnostics["splat_count"],
    )

snapshot = backend.snapshot()

print()
print("Final map frame:", snapshot.frame.value)
print("Total splats in map:", len(snapshot))
print("First splat:", snapshot.splats[0])

# %% [markdown]
# ## Cell 5 — Run a benchmark
#
# A benchmark turns the run into a JSON-ready report.
# This is useful when comparing future real backends.

# %%
from mosaic.evaluation import run_slam_benchmark

artifact = run_slam_benchmark(
    scenario=scenario,
    backend=DeterministicSplatBackend(map_frame=FrameId("map")),
)

pprint(artifact.as_dict())

# %% [markdown]
# ## Cell 6 — Add regression gates
#
# A regression gate is a simple rule like:
# "tracking success must be at least 100%" or "splat count must be at least 5."

# %%
from mosaic.evaluation import FailureClass, RegressionGate, check_regression_gates

gates = (
    RegressionGate(
        metric_name="tracking_success_rate",
        minimum=1.0,
        failure_class=FailureClass.LIFECYCLE,
    ),
    RegressionGate(
        metric_name="splat_count",
        minimum=5.0,
        failure_class=FailureClass.MAP_FUSION,
    ),
)

results = check_regression_gates(artifact, gates)

for result in results:
    pprint(result.as_dict())

# %% [markdown]
# ## Cell 7 — Fuse two maps together
#
# Fusion combines maps while preserving provenance.
# Provenance means Mosaic remembers where each map piece came from.

# %%
from mosaic.fusion import FusionInput, ProvenancePreservingFusion

backend_a = DeterministicSplatBackend(map_frame=FrameId("map"))
backend_b = DeterministicSplatBackend(map_frame=FrameId("map"))

for observation in synthetic_forward_sequence(frame_count=3).sequence:
    backend_a.process(observation)

for observation in synthetic_forward_sequence(frame_count=2).sequence:
    backend_b.process(observation)

map_a = backend_a.snapshot()
map_b = backend_b.snapshot()

fusion = ProvenancePreservingFusion()
fusion_result = fusion.fuse(FusionInput(maps=(map_a, map_b)))

print("Fusion strategy:", fusion.name)
print("Fusion status:", fusion_result.status.value)
print("Input map A splats:", len(map_a))
print("Input map B splats:", len(map_b))
print("Fused map splats:", len(fusion_result.fused_map))

print()
print("Provenance counts:")
pprint(dict(fusion_result.provenance.per_provenance_counts))

print()
print("Diagnostics:")
pprint(dict(fusion_result.diagnostics))

# %% [markdown]
# ## Cell 8 — Ask agent-style questions about the map
#
# Agent-friendly queries return small typed answers.
# They do not dump the whole raw map.

# %%
from mosaic.agents import LocalRadiusQuery, SplatPosteriorView

view = SplatPosteriorView(fusion_result.fused_map)

print("Posterior summary:")
print(view.summary())

print()
print("Uncertainty summary:")
print(view.uncertainty())

print()
print("Provenance summary:")
pprint(dict(view.provenance().counts))

print()
print("Local geometry query near x=0:")
query = LocalRadiusQuery(
    center=(0.0, 0.0, 1.0),
    radius=0.25,
    max_results=10,
)

query_result = view.query_local(query)
print(query_result)
print("Matching splat IDs:", query_result.splat_ids)

# %% [markdown]
# ## Cell 9 — Save benchmark output as JSON
#
# This writes the benchmark report to disk so another tool can read it.

# %%
from mosaic.evaluation import write_benchmark_artifact

output_path = Path("mosaic-demo-benchmark.json")
write_benchmark_artifact(artifact, output_path)

print("Wrote:", output_path.resolve())
print(output_path.read_text())
