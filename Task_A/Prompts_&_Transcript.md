# Task A — Prompt and Transcript Log

**LLM:** ChatGPT  
**Model:** GPT-6  
**Date:** 20 October 2026  
**System:** SmartBrew AI

This document records the prompts used to generate the first versions of the requirements, user stories, and product backlog. The original AI-generated artifacts are kept separate from the later evaluation and revision process.

---

## Prompt 1: Functional and Non-Functional Requirements

**Purpose:** Generate functional and non-functional requirements using the original SmartBrew AI description and the requirements format from Lab 2.

**Prompt strategy:** Role prompting, explicit constraints, source grounding, and output-format instructions.

### Prompt used

Act as a software requirements engineer helping with a university Software Engineering assignment.

TASK  
Generate functional requirements and non-functional requirements for the SmartBrew AI system described earlier in this conversation.

SOURCE  
Use the original SmartBrew AI system description I provided earlier as the primary source. Also consider my original Lab 2 Task 2b requirements table to understand the required format and level of detail.

CONTEXT  
My original Lab 2 work includes 12 user stories and 12 functional requirements. My own feature, added in Lab 1, is an LLM-based natural-language beverage assistant that translates users' drink requests into customization instructions.

INSTRUCTIONS
1. Separate functional requirements (what the system must do) from non-functional requirements (quality attributes and constraints).
2. Preserve the Lab 2 functional-requirement table structure: ID, Description, Inputs, Outputs, Precondition, Postcondition.
3. Give functional requirements IDs FR-01, FR-02, etc., and non-functional requirements IDs NFR-01, NFR-02, etc.
4. Cover the functionality explicitly stated in the original system description, including accounts, preferences, transaction records, custom recipes, recommendations, mood detection, the touchscreen menu, ingredient thresholds, payments, receipts, technician functions, diagnostics, privacy, network failures, and the optional local LLM assistant.
5. For non-functional requirements, identify relevant quality attributes and constraints, such as privacy, security, reliability, performance, and usability, only where supported by the description or reasonably necessary for the system.
6. Do not invent specific numerical targets, technologies, features, or guarantees that the source does not establish. If a measurable target or implementation detail is missing, mark it as unspecified or identify it as an assumption requiring confirmation.
7. Keep each requirement clear, specific, and independently understandable. Avoid unnecessary duplication.
8. Do not assume that optional functionality is mandatory. Explicitly identify optional features.
9. After the tables, list ambiguities and assumptions that need stakeholder confirmation.
10. Do not compare the results with my original work yet. This response is only the AI-generated requirements artifact.

OUTPUT  
First provide the functional requirements table using the required columns. Then provide a separate non-functional requirements table. Finally, provide a short list of unresolved questions and assumptions.

Keep the language clear and suitable for a bachelor's-level Software Engineering assignment.

### First-generation LLM response

The original response is recorded in `Functional_NonFunctional_Requirements.md`.

It contains:
- Functional requirements FR-01 to FR-17.
- Non-functional requirements NFR-01 to NFR-10.
- A list of unresolved questions and assumptions.

The original response covers accounts, login, preferences, beverage browsing and customization, ingredient availability, recipes, recommendations, mood analysis, the optional natural-language assistant, payments, transaction recording, receipts, administrative access, inventory, waste monitoring, diagnostics, and fallback operation.

### Evaluation

The generated requirements cover most of the system's stated functionality. However, some quality requirements are vague, some security requirements overlap with functional requirements, and certain details—such as offline payments, performance targets, and data retention—need clarification. These issues were considered during the subsequent review.

---

## Prompt 2: User Stories

**Purpose:** Generate user stories from the original SmartBrew AI description, the Lab 2 user stories, and the AI-generated requirements.

**Prompt strategy:** Source grounding, explicit user-story format, actor identification, scope constraints, and instructions to preserve optional functionality.

### Prompt used

Act as a software requirements engineer helping with a university Software Engineering assignment.

TASK

Generate user stories for the SmartBrew AI system described earlier in this conversation.

SOURCE

Use the original SmartBrew AI system description and my original Lab 2 Task 2b user stories as the primary sources. Also consider the AI-generated functional and non-functional requirements generated earlier in this conversation.

CONTEXT

My original Lab 2 work contains 12 user stories, US-01 to US-12, covering account management, login, beverage preferences, browsing and customization, custom recipes, recommendations, mood and weather, a natural-language assistant, payments, receipts, inventory, and maintenance.

My own feature, added in Lab 1, is an LLM-based natural-language beverage assistant that translates a user's drink request into beverage customization instructions.

INSTRUCTIONS
1. Generate a complete set of user stories covering the system's stated functionality.
2. Use the format: ID, Title, and User Story.
3. Write each user story using the structure: “As a [type of user], I want [goal], so that [benefit].”
4. Use appropriate actors, including ordinary users and technicians where relevant.
5. Cover the functionality in the original system description, including accounts, preferences, transaction records, custom recipes, recommendations, mood detection, the touchscreen menu, ingredient availability, payments, receipts, technician functions, diagnostics, and the natural-language assistant.
6. Preserve the optional status of the local LLM assistant. Do not make optional functionality mandatory.
7. Avoid duplicating stories that represent essentially the same user goal. Separate stories when they represent meaningfully different goals or actors.
8. Do not invent unsupported functionality or specific implementation details.
9. Keep the stories clear, concise, and suitable for a bachelor's-level Software Engineering assignment.
10. Do not compare the generated stories with my original Lab 2 stories yet. Do not provide a critique or recommendations.
11. After the table, list any important ambiguities or assumptions that need stakeholder confirmation.

OUTPUT

Provide one user-story table with columns ID, Title, and User Story, followed by a short list of unresolved questions and assumptions.

Keep the output focused on the requested artifact.

### First-generation LLM response

The first-generation response contains 20 user stories, US-01 to US-20, followed by an optional-feature note and unresolved questions.

The stories cover account management, login, preferences, beverage browsing and customization, ingredient availability, custom recipes, personalized recommendations, mood-based recommendations, the optional natural-language assistant, confirmation of assistant suggestions, payment, receipts, transaction recording, ingredient inventory, inventory-counter reset, waste monitoring, overflow protection, diagnostics, secure administrative access, and fallback operation.

**Original response location:** `User_Stories.md`.

To preserve the original wording, use the user-story table in that file as the response transcript. Do not substitute revised stories from the later review.

### Evaluation

The generated stories cover the main user goals and make some behaviors more explicit than the original set. However, some stories may be too narrow or describe system mechanisms rather than independent user goals. The transaction-recording story must not imply a user-facing transaction-history feature unless that feature is confirmed. Mood analysis should be described as estimating mood, and the optional status of the natural-language assistant must be retained.

---

## Prompt 3: Product Backlog

**Purpose:** Generate a product backlog using the original SmartBrew AI description and the Lab 2 backlog format.

**Prompt strategy:** Source grounding, explicit table structure, preliminary estimation, demonstration scenarios, and instructions to identify assumptions and optional functionality.

### Prompt used

Act as a software requirements engineer helping with a university Software Engineering assignment.

TASK

Generate a product backlog for the SmartBrew AI system described earlier in this conversation.

SOURCE

Use the original SmartBrew AI system description and my original Lab 2 Task 2b product backlog as the primary sources. Also consider the AI-generated functional and non-functional requirements and user stories generated earlier in this conversation.

CONTEXT

My original Lab 2 product backlog contains 12 items corresponding to user stories US-01 to US-12. Its columns are ID, Name, Imp, Est, How to demo, and Notes.

In the original backlog:
- Imp represents importance, with 1 being highest and 12 being lowest.
- Est represents estimated effort in story points.
- How to demo describes how the feature can be demonstrated.
- Notes contains additional relevant information.

INSTRUCTIONS
1. Create a product backlog that covers the system's main functionality.
2. Use the exact columns: ID, Name, Imp, Est, How to demo, Notes.
3. Give each item a unique ID and a clear, concise name.
4. Use importance rankings where 1 is the highest priority. If there are more than 12 items, provide a consistent ranking across all items.
5. Provide plausible relative effort estimates in story points. These are preliminary estimates, not measured values.
6. Give each item a concrete demonstration scenario that shows how its functionality works.
7. Use the Notes column to identify relevant assumptions, dependencies, optional functionality, or uncertainties.
8. Preserve the optional status of the local LLM natural-language assistant.
9. Avoid duplicating backlog items that represent essentially the same functionality.
10. Do not invent unsupported features, technologies, numerical targets, or guarantees.
11. Do not treat the generated importance rankings or effort estimates as objectively correct. They are initial proposals requiring review.
12. Do not compare the generated backlog with my original Lab 2 backlog yet. Do not provide a critique or recommendations.
13. Keep the output suitable for a bachelor's-level Software Engineering assignment.

OUTPUT

Provide one product-backlog table using the six required columns. After the table, briefly list any important assumptions or uncertainties that affect the backlog estimates or priorities.

Keep the output focused on the requested artifact.

### First-generation LLM response

The original response is recorded in `Product-Backlog.md`.

It contains 16 backlog items, PB-01 to PB-16, using the six required columns: ID, Name, Imp, Est, How to demo, and Notes. The response also includes assumptions and uncertainties.

The items cover payment, browsing and customization, account management, login, preferences, custom recipes, personalized recommendations, the optional natural-language assistant, mood-based recommendations, receipts, ingredient inventory, maintenance and monitoring, transaction recording, ingredient availability control, fallback operation, and secure administrative access.

### Evaluation

The generated backlog follows the requested format and provides demonstration scenarios, dependencies, and uncertainties. However, all six additional items were ranked below the original 12 without sufficient justification. The rankings therefore require review. Effort estimates should remain preliminary, and demonstrations should use observable results. Dependencies between inventory and ingredient availability, and between recommendation features, should also be considered.

---

## Note on the transcript

The files `Functional_Nonfunctional_Requirements.md`, `User_Stories.md`, and `Product-Backlog.md` contain the first-generation artifact outputs. They should remain unchanged as records of the initial generation. Revised accepted artifacts and the critical comparison should be maintained separately.