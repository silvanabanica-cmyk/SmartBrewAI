# Task A — Final User Stories for SmartBrew AI

The original AI-generated user stories were reviewed against the SmartBrew AI system description. The revised stories retain the main user goals, remove unnecessary separation between closely related activities, and clarify where functionality is optional or needs confirmation.

| ID | Title | User Story |
|---|---|---|
| US-01 | Account Management | As a user, I want to create and manage my account, so that my account information can be maintained by the system. |
| US-02 | Login | As a registered user, I want to log in using supported credentials or an NFC card, so that I can access my account. |
| US-03 | Beverage Preferences | As a user, I want to manage my beverage preferences, so that the system can use them when preparing drinks and making recommendations. |
| US-04 | Browse and Customize Beverages | As a user, I want to browse beverage categories, view nutritional information, and customize a drink, so that I can choose a beverage that suits my needs. |
| US-05 | Ingredient Availability | As a user, I want to know whether a beverage is available, so that I do not attempt to order a drink that cannot be prepared. |
| US-06 | Custom Recipes | As a user, I want to save, name, modify, and reuse custom beverage recipes, so that I can order drinks I enjoy more easily. |
| US-07 | Personalized Recommendations | As a user, I want to receive recommendations based on my preferences, previous orders, time of day, and available weather information, so that I can discover suitable beverages. |
| US-08 | Mood-Based Recommendations | As a user, I want the system to adapt recommendations using optional camera-based mood estimation, so that I can receive suggestions that may suit how I feel. |
| US-09 | Natural-Language Beverage Assistant | As a user, I want to describe the drink I want in natural language, so that the optional assistant can suggest a suitable beverage configuration. |
| US-10 | Review Assistant Suggestions | As a user, I want to review and modify the assistant's suggested configuration before ordering, so that I remain in control of my beverage choice. |
| US-11 | Payment | As a user, I want to pay using a supported payment method, so that I can complete my beverage purchase. |
| US-12 | Receipt | As a user, I want to receive a receipt by QR code or email after a completed transaction, so that I can access a record of my purchase. |
| US-13 | Transaction Recording | As a system operator, I want completed transactions and their customization details to be recorded, so that the system can support personalization and transaction record-keeping. |
| US-14 | Inventory Management | As a technician, I want to monitor ingredient levels, register refills, and reset relevant counters, so that inventory information reflects maintenance activities. |
| US-15 | Waste Monitoring and Overflow Protection | As a technician, I want the system to monitor liquid waste and coffee grounds, alert me when disposal is needed, and stop operation if overflow occurs, so that waste containers can be managed safely. |
| US-16 | Error Monitoring and Diagnostics | As a technician, I want to view error messages and event logs, so that I can investigate faults and support remote diagnostics. |
| US-17 | Secure Administrative Access | As an authorized technician, I want to access administrative functions using an approved access method, so that maintenance functions are restricted to authorized personnel. |
| US-18 | Fallback Operation | As a user, I want basic manual ordering to remain available during network or external-service failures, so that I can continue using supported machine functions. |

## Optional Features and Assumptions

- US-09 and US-10 apply only when the optional local LLM assistant is installed and enabled.
- US-08 depends on the optional camera-based mood-estimation feature. User consent and opt-out behavior require confirmation.
- Payment availability during network failures is not fully specified and should not be assumed.
- US-13 concerns recording completed transactions. It does not assume that users can view a transaction-history screen, because that functionality is not explicitly specified.
- Importance rankings, implementation priorities, and acceptance criteria should be decided separately during backlog refinement.