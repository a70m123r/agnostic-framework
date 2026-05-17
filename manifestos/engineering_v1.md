# Agnostic: A Structural Vocabulary for External Actors in Multi-Agent Systems

**Agnostic manifesto, v1 — software engineer edition**
**Status:** draft for review. Critic-writer subagent produced this with full framework corpus context; revision notes preserved at the end.

---

Your multi-agent system has a blind spot. It knows how to orchestrate tasks, manage memory, call tools, and route messages between agents. What it doesn't know is anything about the external systems it's operating inside. When a platform's ranking logic shifts, when a regulatory system changes its classification rules, when an internal recommendation engine starts behaving differently — your agents notice the downstream effect and retry. They don't model the cause.

That's the gap Agnostic fills. Not orchestration. Not memory. Not tool-use. A structural vocabulary for maintaining explicit, evolving models of external strategic actors — algorithms, platforms, institutions, other agent systems — as first-class data structures in your multi-agent stack.

---

## The Gap in Existing Frameworks

AutoGen gives you conversable agents and group chats. CrewAI gives you role-based task delegation. LangGraph gives you stateful DAGs with cycles. All of them give you control over what's inside your system. None of them give you a model of what's outside it.

When your LangGraph agent hits Google's search API and gets a different results distribution than yesterday, it has no place to put that observation except a retry loop or a log line. There's no slot in the framework's data model for "my model of Google's current ranking behavior." There's no schema for "here are three competing hypotheses about why my visibility dropped, with confidence weights." There's no operation for "merge two agents that have independently been modeling the same external actor."

MCP (Model Context Protocol) is worth calling out specifically: MCP gives you a clean interface for tools and resources, but it's a connection protocol, not an epistemics protocol. It tells your agent how to call a function; it doesn't tell your agent what structural model to maintain about the system on the other end of that function.

Agnostic sits alongside these frameworks, not in competition with them. It's the layer that says: here is what to put in your blackboard about the outside world.

---

## External Actors as First-Class Data

The core shift is epistemic. An external actor — Google's PageRank system, an internal content moderation algorithm, a regulatory body, a partner API that changes behavior based on your usage patterns — is not a tool endpoint. It's an agent-like system with its own logic, constraints, and state. Your agent should model it as such.

In Agnostic, an external actor gets a schema with multiple candidate models, not one compiled belief:

```yaml
ExternalActor:
  id: "google_search_ranking_v2"
  candidate_models:
    - model_id: "freshness_weighted"
      harness:
        signals_tracked: ["publication_date", "backlink_velocity", "crawl_frequency"]
        last_probed: "2026-05-12T14:23:00Z"
      wrapper:
        hypothesis: "Ranking currently weights content freshness above domain authority"
        coherence_rules: ["high_freshness_beats_high_DA_on_informational_queries"]
      weight:
        magnitude: 0.71
        spin: 1            # +1 = reinforcing, -1 = contradicting recent observations
        scale: "weekly"
        freshness: 0.88
      compile_confidence: 0.62
    - model_id: "domain_authority_stable"
      harness:
        signals_tracked: ["domain_authority", "anchor_text_diversity"]
        last_probed: "2026-05-10T09:00:00Z"
      wrapper:
        hypothesis: "Domain authority is still the primary long-term ranking signal"
        coherence_rules: ["DA > 50 outranks fresher content on navigational queries"]
      weight:
        magnitude: 0.44
        spin: -1
        scale: "monthly"
        freshness: 0.51
      compile_confidence: 0.31
  scout_queue: ["entity_prominence_model", "eeat_freshness_interaction"]
  consolidated_view:
    dominant_signal: "freshness_weighted"
    confidence: 0.58
    last_rebalanced: "2026-05-13T00:00:00Z"
  last_observed_at: "2026-05-13T08:45:00Z"
```

The key structural decision: `candidate_models` is a list, not a single object. You are not forced to compile a single belief about Google's ranking algorithm. You maintain competing models and let them compete for dominance over time through observation.

---

## The Primitives as Data Structures

### Observer = (harness, wrapper, inner_sandbox, action_space)

An Observer is an agent with four structural slots:

- `harness`: the agent's tool/capability set — what it can call, what APIs it holds
- `wrapper`: system prompt + role + coherence rules — the constraints on what it's allowed to conclude
- `inner_sandbox`: scratchpad / working memory — ephemeral state, hypothesis pool in progress
- `action_space`: the intersection of what the harness permits and what the current context allows

This maps directly to how you'd design an agent class:

```python
@dataclass
class Observer:
    harness: dict[str, Callable]       # tool registry
    wrapper: AgentWrapper              # role, coherence rules, system prompt
    inner_sandbox: HypothesisPool      # working memory + fuzzy candidates
    action_space: list[str]            # computed from harness ∩ current constraints
```

### The AU Matrix

Every Observer has an Agnostic Unit (AU): a weighted matrix where rows are perceivable signals (P) and columns are available actions (A). Each cell is a `WaveletWeight`:

```python
@dataclass
class WaveletWeight:
    magnitude: float      # how strong is this signal-action coupling?
    spin: int             # +1 reinforcing, -1 contradicting
    scale: str            # temporal scale: "hourly", "daily", "weekly"
    freshness: float      # [0,1] — how recent is this weight?

# AU matrix: P × A
au_matrix: dict[tuple[str, str], WaveletWeight]
# e.g., au_matrix[("crawl_frequency_spike", "increase_publish_rate")] = WaveletWeight(0.8, 1, "daily", 0.95)
```

The matrix is not static. Weights decay with freshness, flip spin on contradictory observations, and get updated by scout agents feeding new observations from the field.

### Fuzzy and Canon

- `Fuzzy`: a candidate space — in code, a priority queue of unresolved hypotheses with weights. This is your agent's epistemic scratchpad before it commits to a belief.
- `Canon`: compiled state — the agent's committed knowledge graph. You promote a fuzzy hypothesis to canon when its `compile_confidence` crosses a threshold and survives challenge from competing models.

Carrier artifacts — skill files, code, decision records, model weights — are the durable outputs that survive agent memory resets. Think of them as the compiled build artifacts of your agent's reasoning.

---

## The Multi-Possibility Deposition Pool

When an agent encounters a new pattern or anomaly, the standard approach is: observe → conclude → act. Agnostic proposes: observe → deposit N candidate hypotheses → scout asynchronously → let competition decide.

```python
class HypothesisPool:
    def __init__(self):
        self.pool: list[CandidateModel] = []
        self.scout_queue: asyncio.Queue = asyncio.Queue()

    async def deposit(self, observation: Observation, n_candidates: int = 3):
        """
        Don't commit. Generate N candidate explanations and enqueue for scouting.
        """
        candidates = await self.generate_candidates(observation, n=n_candidates)
        for c in candidates:
            self.pool.append(c)
            await self.scout_queue.put(c.model_id)

    async def scout_worker(self, external_actor: ExternalActor):
        """
        Pull candidates from queue, probe the external actor, update weights.
        """
        while True:
            model_id = await self.scout_queue.get()
            candidate = self.get_candidate(model_id)
            probe_result = await self.probe(external_actor, candidate)
            candidate.weight.magnitude = self.update_magnitude(
                candidate.weight.magnitude, probe_result
            )
            candidate.weight.spin = probe_result.direction
            candidate.weight.freshness = 1.0
            self.rebalance()

    def compile_to_canon(self, threshold: float = 0.75) -> CandidateModel | None:
        """
        Promote dominant candidate to canon if confidence exceeds threshold
        and lead over second-place exceeds margin.
        """
        ranked = sorted(self.pool, key=lambda c: c.compile_confidence, reverse=True)
        if ranked and ranked[0].compile_confidence >= threshold:
            return ranked[0]
        return None  # stay in fuzzy; continue scouting
```

This pattern is recognizable to engineers who've worked with blackboard architectures or belief propagation networks. Multiple knowledge sources write to a shared blackboard; a controller decides what gets promoted to committed state. Agnostic formalizes this for external actor modeling specifically.

---

## Symbiosis-as-Pushout: First-Class Agent Merger

This is the operation missing from every existing framework. If you have two agents that have independently been modeling the same external actor, and their models are compatible (overlapping signal sets, non-contradictory coherence rules), you can merge them into a composite agent.

In category theory terms, this is a pushout: two objects that share a common interface compose into a new object that preserves both. In engineering terms:

```python
def merge_agents(
    agent_a: Observer,
    agent_b: Observer,
    compatibility_check: Callable[[Observer, Observer], bool],
    delta_action_threshold: float = 0.1,
    min_rounds: int = 10
) -> Observer | None:
    """
    Merge two agents if:
    1. Their harnesses are compatible (shared interface)
    2. Net change in action space (delta-A) is positive over K rounds
    3. Coherence rules don't contradict
    """
    if not compatibility_check(agent_a, agent_b):
        return None

    delta_a = compute_delta_action(agent_a, agent_b, rounds=min_rounds)
    if delta_a < delta_action_threshold:
        return None

    merged_harness = merge_harnesses(agent_a.harness, agent_b.harness)
    merged_wrapper = resolve_coherence(agent_a.wrapper, agent_b.wrapper)
    merged_sandbox = HypothesisPool.merge(agent_a.inner_sandbox, agent_b.inner_sandbox)
    merged_action_space = list(set(agent_a.action_space) | set(agent_b.action_space))

    return Observer(
        harness=merged_harness,
        wrapper=merged_wrapper,
        inner_sandbox=merged_sandbox,
        action_space=merged_action_space
    )
```

The condition that makes this non-trivial is `delta_a`: you only merge if the merged agent's action space is meaningfully larger than either parent's. This prevents degenerate merges where you're just duplicating state. The biological analog is endosymbiosis (eukaryogenesis); the engineering analog is microservice consolidation under a unified API surface — not performed by default, only when the interface contract justifies it.

---

## The Slow-Fast Pushout: Reservoir Computing as Architecture

Agnostic's preferred architectural template for multi-agent systems is the slow-fast pushout: a slow strategist agent paired with fast scout agents.

- **Slow strategist**: large context window, high memory depth, slow update cycle. Maintains canon, manages ExternalActor models, decides when to promote fuzzy hypotheses.
- **Fast scouts**: small context window, fast processing, narrow focus. Probe external actors, return observations, feed the hypothesis pool.

This is reservoir computing in architectural form. The reservoir (slow strategist's accumulated state) is rich and high-dimensional; the readout (fast scout output) is sparse and targeted. The two layers don't need to be in lock-step. Scouts run asynchronously; the strategist rebalances periodically.

```python
async def run_slow_fast_system(
    strategist: Observer,
    scouts: list[Observer],
    external_actors: list[ExternalActor],
    rebalance_interval_seconds: int = 300
):
    # Launch scouts as async workers
    scout_tasks = [
        asyncio.create_task(scout.run_probe_loop(external_actors))
        for scout in scouts
    ]

    # Strategist rebalances on interval
    while True:
        await asyncio.sleep(rebalance_interval_seconds)
        for actor in external_actors:
            strategist.inner_sandbox.rebalance()
            canon_candidate = strategist.inner_sandbox.compile_to_canon()
            if canon_candidate:
                strategist.update_canon(actor.id, canon_candidate)
```

The criticality metric Γ = connect_rate / (prune_rate + stabilize_rate) gives you a system health signal. Target Γ ≈ 1. If your scouts are creating hypotheses faster than the strategist can prune and stabilize them, Γ > 1 and you're in overload: noise accumulates, canon drifts. If the strategist is over-pruning relative to new signal, Γ < 1 and the system is stagnant.

---

## Worked Example: Modeling a Search Algorithm

Say you're building a content distribution agent that autonomously places content across platforms and optimizes for visibility. The agent needs to model Google's current ranking behavior — not as a static API contract, but as an evolving system with uncertain internal state.

Here's what the agent's main loop looks like with Agnostic primitives:

```python
async def content_agent_main():
    google = ExternalActor(
        id="google_search_2026",
        candidate_models=[],
        scout_queue=[],
        consolidated_view={},
        last_observed_at=None
    )

    strategist = Observer(
        harness={"publish": publish_fn, "query_serp": serp_fn, "annotate": annotate_fn},
        wrapper=AgentWrapper(
            role="content_strategist",
            coherence_rules=["never_publish_without_hypothesis_validation"]
        ),
        inner_sandbox=HypothesisPool(),
        action_space=["publish", "query_serp", "annotate"]
    )

    scouts = [
        Observer(harness={"query_serp": serp_fn}, wrapper=AgentWrapper(role="serp_scout"), ...),
        Observer(harness={"fetch_metrics": metrics_fn}, wrapper=AgentWrapper(role="metrics_scout"), ...)
    ]

    # Day 1: First observation — SERP position dropped 4 places overnight
    observation = Observation(
        signal="serp_rank_drop",
        delta=-4,
        context={"query": "content automation tools", "timestamp": "2026-05-13T08:00:00Z"}
    )

    # Don't commit to one explanation. Deposit three candidates.
    await strategist.inner_sandbox.deposit(observation, n_candidates=3)
    # Pool now contains: freshness_model, competitor_activity_model, algo_update_model

    # Scouts probe over next 6 hours and feed back weight updates
    await run_slow_fast_system(strategist, scouts, [google])

    # After scouting, compile if confident
    canon = strategist.inner_sandbox.compile_to_canon(threshold=0.70)
    if canon:
        # Update the ExternalActor's consolidated view
        google.consolidated_view = {
            "dominant_model": canon.model_id,
            "confidence": canon.compile_confidence,
            "recommended_action": canon.wrapper.coherence_rules
        }
        # Now plan content based on committed belief
        plan = await strategist.plan_content_strategy(google.consolidated_view)
    else:
        # Stay in fuzzy; keep scouting; don't act on incomplete signal
        log.info("No dominant model yet. Continuing to scout.")
```

The role taxonomy matters here. A scout agent is declared with `role="serp_scout"`. That role constrains its permitted interactions — it can probe and report, not plan or publish. A `role="verifier"` agent can check canon candidates against new observations but cannot generate new hypotheses. These aren't soft guidelines; they're enforced coherence rules in the wrapper that constrain the `action_space` computation.

---

## Where Agnostic Fits in Your Stack

Think of it as a layer between your orchestration framework and your tool endpoints:

```
[AutoGen / CrewAI / LangGraph]   ← orchestration, routing, memory
        ↓
[Agnostic primitives]            ← external actor models, hypothesis pools, AU matrices
        ↓
[MCP / tool endpoints]           ← actual API calls, data retrieval
```

MCP gives you the connection. LangGraph gives you the state machine. Agnostic gives you the epistemics — the structured beliefs about what's on the other end of the connection, and how to update them.

You can adopt Agnostic incrementally. Start with just the ExternalActor schema. Add it as a LangGraph state node. When your agent observes an anomaly, write to the `candidate_models` list instead of directly updating a single belief field. That's it. That's the smallest useful adoption.

---

## Where the Framework Is Incomplete

Be direct about this: Agnostic is a specified vocabulary, not a production library.

There is no `pip install agnostic` today. The AU matrix weights (WaveletWeight) are conceptually motivated but not empirically calibrated — there is no benchmarked learning rule for how spin should flip or how freshness should decay across different probe intervals. The compile_to_canon threshold of 0.75 is illustrative, not the result of tuning experiments. The criticality metric Γ has an elegant form but no operational guidance yet for what probe rates and prune rates to target in practice.

Symbiosis-as-pushout (agent merger) is the most speculative primitive. The `delta_action_threshold` and `min_rounds` parameters exist in the spec but have no reference implementation or ablation study. The claim that compatible agents can be merged into a net-positive composite is theoretically motivated but untested at scale.

The cross-substrate transfer use case (protein language models on network packets) is a research aspiration in the framework's lineage, not a practical pattern for most readers of this document.

What is solid: the ExternalActor schema, the HypothesisPool mechanic, the slow-fast pushout architecture, and the role taxonomy. These are immediately adoptable as design patterns, regardless of whether a full framework exists.

---

## Where to Start

Pick one primitive. The smallest useful adoption:

1. **Add an ExternalActor schema to your LangGraph state** for any external system your agents interact with. Give it a `candidate_models` list instead of a single `current_model` field. You've just built the core of the pattern.

2. **Replace single-belief updates with deposition.** When an anomaly occurs, resist the urge to immediately update your agent's state with one explanation. Write three candidate explanations to a pool. Let subsequent observations weight them. Promote the winner after K observations.

3. **Declare role constraints in your wrapper** before you deploy. A scout can scout. A verifier can verify. Write that as an enforced rule in the agent's coherence_rules, not a comment in the system prompt.

4. **Instrument Γ.** Even informally. Track how many new hypotheses your system generates per hour versus how many it prunes or stabilizes. If generation consistently outpaces resolution, your system is in overload — even if it looks busy and productive.

The ideas in Agnostic aren't foreign to engineers who've worked with blackboard architectures, belief propagation, or Kalman filters. The contribution is applying this epistemics layer to the specific problem of multi-agent systems that operate inside external strategic environments — and giving you concrete schemas, data structures, and architectural templates rather than metaphors.

The external systems your agents operate inside are not static APIs. Model them that way.

---

## Critic-writer revision notes

**Code that was illustrative-but-not-quite-real.** The first draft had pseudocode that elided too many details — particularly around the HypothesisPool's `generate_candidates` and `probe` methods, which were called without any hint of implementation. The revision makes the scaffolding more explicit (async queue, proper dataclass signatures) while explicitly leaving internal methods as stubs, rather than pretending they are implemented. This is more honest and more useful: engineers can see where to fill in their own logic.

**The WaveletWeight was hand-wavy.** The first draft introduced WaveletWeight with field names but no explanation of what spin means operationally. The revision adds "+1 reinforcing, -1 contradicting" inline and explains that spin flips on contradictory observations — still incomplete as an implementation, but no longer opaque as a concept.

**The ExternalActor schema needed to show why candidate_models is a list.** The first draft showed the schema without enough surrounding text explaining why the structural decision matters. The revision leads with "you are not forced to compile a single belief" immediately after the schema block, connecting the data structure to the design principle.

**The MCP positioning was too vague.** The first draft said MCP was "orthogonal." The revision makes the distinction sharper: "MCP gives you the connection. Agnostic gives you the epistemics." And the stacked diagram makes the layer relationship concrete.

**The honesty section needed more specificity.** The first draft said "no production implementation" but didn't enumerate which parts of the spec are most uncertain. The revision calls out specifically: the Γ metric has no operational tuning guidance, the merge threshold is illustrative, and the cross-substrate transfer case is a research aspiration rather than a practical pattern. Skeptical engineers will reject a framework faster for overstating readiness than for honest incompleteness.

**The call to action was too abstract.** "Try one primitive" without specifying which primitive is not actionable. The revision gives four specific entry points ordered from easiest to least essential, each tied to a concrete implementation step rather than a concept.
