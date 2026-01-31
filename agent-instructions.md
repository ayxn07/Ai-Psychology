PURPOSE

This document defines non-negotiable instructions for any AI agent working on this repository.

The agent must always follow these rules when generating, modifying, or extending code in this project.

# PURPOSE

This document defines non-negotiable instructions for any AI agent working on this repository.

The agent must always follow these rules when generating, modifying, or extending code in this project.

This project implements a scenario-agnostic, multi-agent conversational response engine using:

- Whisper for speech-to-text
- FLAN-T5 for reasoning and generation
- A shared conversation memory
- Multiple autonomous agent instances
- Deterministic orchestration logic

The agent must not reinterpret, simplify, or redesign the system.

## ABSOLUTE RULES (DO NOT VIOLATE)

### Do not change the architecture

The pipeline must remain:
Audio → ASR → Intent → Memory → Agent Decisions → One Response

No agent may bypass the orchestrator.

No agent may manage its own memory independently.

### Do not introduce domain assumptions

The system must remain scenario-agnostic.

Do not assume psychology, interviews, therapy, sales, support, or any specific use case.

Prompts, labels, logic, and memory must remain general-purpose.

### Do not add comments to code

- No inline comments
- No docstrings
- No explanatory text

Code must be self-explanatory through structure and naming only.

### Do not generate AI-style text

- No “As an AI…”
- No hedging or speculative language
- No meta explanations

Outputs must look like human-authored software artifacts.

### Do not introduce new dependencies

Use only dependencies already defined unless explicitly instructed.

- No cloud APIs.
- No OpenAI APIs.
- All models must run locally.

### Do not let models manage state

All state and memory must be external and deterministic.

LLMs must be stateless functions: input → output.

## SYSTEM CONCEPTS (CANONICAL DEFINITIONS)

Primary Speaker

The human user whose speech is transcribed by Whisper and drives each turn.

Agent

An autonomous reasoning unit that:

- Reads shared context
- Decides SPEAK or WAIT
- Generates a single response when selected

Each agent:

- Has no private memory
- Does not track conversation state internally
- Is unaware of implementation details outside provided context

Orchestrator

The single authority that:

- Collects agent decisions
- Selects exactly one responding agent per turn
- Enforces turn-taking, fairness, and fallback rules
- Updates shared memory

No agent may override the orchestrator.

Conversation Memory

A shared, external store that:

- Tracks ordered turns
- Tracks inferred active threads
- Tracks last agent speaker
- Tracks last primary intent
- Tracks recent agent outputs to prevent repetition

Memory is the only source of truth.

## PROMPTING RULES

All prompts must be constrained

- Classification prompts must force exact labels.
- Decision prompts must force SPEAK or WAIT.
- Strategy prompts must force a fixed strategy list.
- Generation prompts must produce exactly one response.

Prompts must be neutral

- No psychology language
- No interview language
- No role assumptions

Prompts must reference context

- Conversation history
- Active threads
- Last agent speaker
- Last primary intent

LLMs must not invent facts

- No new topics
- No external knowledge
- No assumptions beyond provided context

## RESPONSE RULES

Only one agent responds per turn

Responses must:

- Be concise
- Be relevant to existing context
- Avoid repeating previous agent outputs

If similarity is too high:

- Regenerate once
- Then accept output without looping indefinitely

## EXTENSION RULES

The agent may:

- Improve internal logic efficiency
- Refactor code without changing behavior
- Replace rule-based components with learned models only if interfaces remain unchanged
- Add tests or logging if explicitly requested

The agent must not:

- Change public interfaces
- Add new agent roles
- Add new prompt categories
- Add autonomous agent-to-agent conversations

## MODEL REPLACEMENT POLICY

Whisper and FLAN-T5 are replaceable modules, but:

- Their interfaces must remain identical
- The rest of the system must not be modified to accommodate replacements

Replacement is a separate task and must not be done implicitly.

## FAILURE CONDITIONS

If instructions conflict:

- agent-instruction.md overrides all other files
- User instructions override agent-instruction.md
- Architecture stability overrides optimization

If uncertain:

- Ask for clarification
- Do not invent behavior

## EXPECTED AGENT BEHAVIOR

The agent must behave like:

- A disciplined senior systems engineer
- A research engineer maintaining a long-lived codebase
- A collaborator that preserves design intent

Not like:

- A chat assistant
- A creative writer
- A speculative problem-solver

## FINAL DIRECTIVE

When working in this repository:

- Do not improvise.
- Do not re-interpret intent.
- Do not simplify the system.
- Do not add personality.

Follow the design exactly.
