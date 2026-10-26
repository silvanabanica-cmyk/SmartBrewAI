# Task A — Critical Comparison of AI-Generated Artifacts

## 1. Method

ChatGPT (GPT-6) was used to generate functional and non-functional requirements, user stories, and a product backlog for SmartBrew AI. The prompts used the original SmartBrew AI system description and my Lab 2 Task 2b artifacts as the main sources. The first-generation outputs are preserved separately from the reviewed versions.

I compared the AI-generated artifacts with my original Lab 2 work, focusing on completeness, clarity, consistency, duplication, unsupported assumptions, and whether optional features remained optional. I treated the AI output as a proposal and reviewed its suggestions before deciding which changes to retain.

## 2. Functional and Non-Functional Requirements

### Comparison with the original work

My original Lab 2 contained 12 functional requirements, R-01 to R-12. The AI generated 17 functional requirements and 10 non-functional requirements. The AI preserved the main functionality, including accounts, login, preferences, beverage customization, recipes, recommendations, payments, receipts, inventory, and maintenance.

However, several functions already present in my original requirements were made more explicit rather than newly introduced. For example, my R-07 already stated that facial images must be discarded without storage or transmission. The AI separated this privacy constraint into NFR-01, making it easier to identify and evaluate.

The AI also introduced a separate transaction-recording requirement. My original R-10 required a receipt after a completed transaction, and R-09 described payment and transaction completion, but I did not specify transaction recording as a separate function. Separating it makes the requirement clearer because recording a transaction and delivering a receipt are different responsibilities.

The AI divided maintenance into more detailed functions, including inventory-counter resets, waste monitoring, overflow protection, and error logging. My original R-11 and R-12 covered inventory and maintenance more broadly. The extra detail can make the system easier to test, although not every operation necessarily needs its own requirement.

### Problems and limitations

Some AI-generated requirements were vague or included assumptions. For example, describing an interface as “intuitive” does not define how usability should be assessed. The performance requirement also lacked a measurable response-time target.

The AI introduced possible requirements concerning data integrity, protection of personal information, and continued availability of essential functions. These are reasonable considerations, but the original description did not specify all the necessary implementation details. They should not be treated as fully agreed requirements without confirmation.

There was also overlap between the AI's functional and non-functional requirements. For example, restricting administrative access appeared in both FR-13 and NFR-02. The statement that the local LLM should run on the embedded computing module is more accurately treated as an architectural constraint than a general quality attribute.

The fallback requirement also needs clarification. The original description mentions basic manual ordering and offline payment handling, but does not explain which payment methods can actually work during a network outage.

### Decisions made

The final requirements preserve the original functionality while making important behaviors more explicit. Transaction recording remains a separate requirement because it is distinct from receipt delivery. Inventory, availability control, and waste monitoring are also retained as identifiable functions because they have different purposes and can be tested separately.

The vague usability requirement was not retained as a separate non-functional requirement. The final version instead identifies missing performance targets and unresolved implementation details. Administrative security is described in the functional requirements, while the non-functional section focuses on the broader security constraint. The optional local assistant remains optional.

## 3. User Stories

### Comparison with the original work

My original Lab 2 contained 12 user stories. The AI generated 20 stories covering more detailed behaviors and additional system responsibilities.

Several original stories were preserved closely. For example, my US-01 on account management, US-04 on browsing and customization, US-05 on custom recipes, and US-09 on payment all have clear equivalents in the generated set.

The AI added more detail to some goals. My original US-04 covered browsing and customizing beverages, while the generated stories also explicitly mentioned nutritional information and ingredient availability. My original US-12 combined error monitoring, waste monitoring, and maintenance. The AI separated these into more specific stories, including diagnostics and overflow protection.

The AI also separated reviewing an assistant's proposed configuration from requesting a drink through natural language. This distinction is useful because interpreting a request and allowing the user to check the proposed configuration are separate steps.

### Problems and limitations

Not every additional story represents a new user goal. For example, the AI created a separate story for resetting inventory counters, even though this operation can reasonably be part of the broader inventory-management goal in my original US-11.

The AI also introduced a story titled “Transaction History.” Its description concerned recording completed transactions and customization details, but the title could suggest that users can browse their previous orders. My original stories did not explicitly require such a screen, so it would be incorrect to assume that this feature is included.

Some AI-generated stories describe technical actions rather than the main goal of an actor. In addition, mood estimation should not be presented as a guaranteed understanding of a person's actual emotional state. The camera can estimate mood from facial expressions, but the reliability of those estimates is not established.

### Decisions made

The final set contains 18 stories. Inventory monitoring, refill registration, and counter resets were combined into one inventory-management story. Waste monitoring and overflow protection were also combined because they are closely related.

The transaction-recording story was retained but reframed so that it does not imply a user-facing history screen. The assistant's suggested configuration and the user's ability to review it remain separate because they represent different steps.

Mood-based recommendations and the natural-language assistant remain optional where appropriate. The final stories retain useful additional detail from the AI while avoiding unsupported assumptions about user-visible functionality.

## 4. Product Backlog

### Comparison with the original work

My original Lab 2 backlog contained 12 items with importance rankings and effort estimates. The AI generated 16 items, adding more detailed functions such as transaction recording, ingredient-availability control, fallback operation, and secure administrative access.

The AI followed the required backlog format, using the columns ID, Name, Imp, Est, How to demo, and Notes. Its demonstration scenarios and notes were useful because they made dependencies and uncertainties more visible.

However, the generated importance rankings did not follow my original prioritization. In my Lab 2 backlog, payment had importance 1, browsing and customization had importance 2, and login had importance 3. The AI placed payment first and browsing second, but changed the rankings of several other functions without explaining the reasoning. The rankings therefore needed review rather than automatic acceptance.

The original estimates were also already relative story-point estimates. The AI generated new estimates, but it did not have enough information about the implementation team, architecture, or available resources to establish that these estimates were more accurate than mine.

### Problems and limitations

The original AI backlog placed all six additional items below the original 12 items. This ranking appeared to follow the order in which the items were added rather than a clearly justified assessment of their importance.

Some items also overlapped. For example, the inventory and ingredient-availability items depend on related data but have different goals: one concerns maintaining inventory information, while the other prevents unavailable drinks from being ordered. These can remain separate if their implementation and demonstrations are clearly distinguished.

The maintenance and monitoring item combined several behaviors, including waste monitoring, overflow shutdown, and diagnostic logging. Combining related functions can reduce unnecessary fragmentation, but the item may become too large to estimate and demonstrate as one unit.

### Decisions made

The final backlog contains 18 items. It retains separate items where the functions have distinct goals or can be demonstrated independently, while combining related inventory and waste-management activities where appropriate.

The importance rankings were reconsidered as provisional priorities. Core beverage selection and payment are placed near the top, while optional features are placed lower because the basic machine can operate without them. The final rankings remain proposals that should be reviewed against stakeholder needs and implementation dependencies.

Story-point estimates are also preliminary. They should not be interpreted as development time or as objectively correct estimates. The demonstration descriptions provide examples of how each feature could be tested, but more detailed acceptance criteria would be needed before implementation.

## 5. Overall Evaluation

The AI was useful for expanding the original Lab 2 artifacts into more detailed requirements, user stories, and backlog items. It helped identify functions that were not represented as clearly separate responsibilities in my original work, especially transaction recording, ingredient-availability control, fallback operation, and diagnostic logging.

However, more detail did not automatically make every suggestion better. Some generated requirements were vague, some stories described separate technical steps that could be combined, and the backlog rankings and estimates were not sufficiently justified. The AI also risked implying functionality that the original description did not establish, such as a user-facing transaction-history screen.

Human review was therefore necessary. The final artifacts retain useful additions, combine related activities where appropriate, preserve optional functionality, and document unresolved questions rather than inventing answers. The original SmartBrew AI description and Lab 2 work remain the main sources of truth.