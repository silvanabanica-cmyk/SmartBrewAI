# Task A — Final Product Backlog for SmartBrew AI

The backlog below is a reviewed proposal based on the original SmartBrew AI description, the Lab 2 backlog, and the AI-generated artifacts. Importance rankings use 1 as the highest priority. Story-point estimates are preliminary relative estimates and should be refined during implementation.

| ID | Name | Imp | Est | How to demo | Notes |
|---|---|---:|---:|---|---|
| PB-01 | Browse and Customize Beverages | 1 | 5 | Browse beverage categories, view nutritional information, customize a drink, and display the resulting configuration. | Core ordering functionality. |
| PB-02 | Payment | 2 | 5 | Select a beverage and a supported payment method; demonstrate the success and failure results. | Payment-service availability and offline payment behavior need confirmation. |
| PB-03 | Login | 3 | 3 | Attempt login with valid and invalid credentials or an available NFC card. | Depends on account management and supported authentication methods. |
| PB-04 | Account Management | 4 | 3 | Create an account and update account information; verify the successful changes. | Account recovery is unspecified. |
| PB-05 | Ingredient Availability Control | 5 | 3 | Configure or simulate an ingredient below its minimum threshold and show that a beverage requiring it cannot be ordered. | Threshold configuration and measurement accuracy need confirmation. |
| PB-06 | Beverage Preferences | 6 | 3 | Change supported preferences and verify that the updated values are saved. | Depends on account/profile functionality where preferences are associated with a user. |
| PB-07 | Transaction Recording | 7 | 3 | Complete a test transaction and verify that the transaction and its customization parameters are recorded. | Retention rules and access permissions need confirmation. |
| PB-08 | Custom Recipes | 8 | 5 | Create and name a recipe, modify it, and select it again. | Depends on beverage customization and recipe storage. |
| PB-09 | Personalized Recommendations | 9 | 5 | Provide sample preferences and previous-order data, then demonstrate recommendations using available time and weather information. | Recommendation scoring and behavior when weather data is unavailable need confirmation. |
| PB-10 | Receipts | 10 | 3 | Complete a test transaction and demonstrate the available QR-code or email receipt method. | Depends on transaction completion and receipt-delivery functionality. |
| PB-11 | Inventory Management | 11 | 5 | Display ingredient levels, register a refill, and reset the relevant counter. | Depends on inventory readings and authorized technician access. |
| PB-12 | Waste Monitoring and Overflow Protection | 12 | 5 | Simulate a waste-container warning and an overflow condition; demonstrate the alert and machine halt. | Thresholds and sensor-failure behavior need confirmation. |
| PB-13 | Error Monitoring and Diagnostics | 13 | 5 | Trigger a test error and show the corresponding administrative dashboard message and event-log entry. | Remote diagnostic details are not fully specified. |
| PB-14 | Secure Administrative Access | 14 | 5 | Demonstrate that an unauthorized access attempt is rejected and an authorized technician can access maintenance functions. | Depends on the selected authorization method. |
| PB-15 | Fallback Operation | 15 | 5 | Simulate a network or external-service failure and demonstrate the basic manual-ordering functions that remain available. | Exact fallback behavior and offline payment support need confirmation. |
| PB-16 | Mood-Based Recommendations | 16 | 8 | In a test environment, provide camera input and demonstrate how an estimated mood affects displayed recommendations. | Depends on camera availability; privacy requirements apply. User consent and opt-out behavior need confirmation. |
| PB-17 | Natural-Language Beverage Assistant | 17 | 8 | Enter a natural-language beverage request and demonstrate the proposed configuration. | Optional local LLM feature; only applies when installed and enabled. |
| PB-18 | Review Assistant Suggestions | 18 | 3 | Review a proposed assistant configuration, modify it, and verify the updated configuration before ordering. | Optional; depends on the natural-language assistant. |

## Backlog Notes

- Importance rankings are initial proposals, not objectively established priorities. They should be reviewed against stakeholder needs and implementation dependencies.
- Story-point estimates are preliminary relative estimates, not measured development times.
- The optional LLM assistant and camera-based mood estimation are retained as separate features rather than assumed to be mandatory.
- A backlog item should be considered complete only when its demonstration produces the expected result. Detailed acceptance criteria can be refined before implementation.
- The backlog does not resolve unspecified behavior, including offline payments, inventory thresholds, recommendation scoring, data retention, and mood-detection consent.