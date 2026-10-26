# Task A — Final Functional and Non-Functional Requirements for SmartBrew AI

This document contains the reviewed requirements based on the original SmartBrew AI system description and the first-generation AI-generated requirements. The requirements have been revised to reduce ambiguity, distinguish functional requirements from quality constraints, and preserve the optional status of the local natural-language assistant.

## 1. Functional Requirements

| ID | Description | Inputs | Outputs | Precondition | Postcondition |
|---|---|---|---|---|---|
| FR-01 | The system shall allow users to create an account and manage their account information. | User account details and requested changes | Account creation or update confirmation, or an error message | The account service is available | The account information is stored or updated if the operation succeeds |
| FR-02 | The system shall allow registered users to log in using supported credentials or an NFC card. | Credentials or NFC card data | Access granted or an error message | The user has a registered account and the required authentication method is available | The user is authenticated or access is denied |
| FR-03 | The system shall allow users to manage beverage preferences, including coffee strength, milk type, temperature, and syrup where supported. | Selected preference values | Updated preference settings or an error message | The user is accessing the relevant settings | Supported preference changes are saved |
| FR-04 | The system shall allow users to browse beverage categories, view nutritional information, and customize beverages through the touchscreen. | Menu selections and customization choices | Beverage information and the selected configuration | The menu is available | The selected beverage configuration is displayed |
| FR-05 | The system shall prevent users from ordering beverages when required ingredients are depleted or below the configured minimum threshold. | Beverage selection and ingredient availability data | Availability information or a message that the beverage cannot be ordered | Ingredient availability data and thresholds are configured | An unavailable beverage cannot proceed to ordering |
| FR-06 | The system shall allow users to save, name, modify, and reuse custom beverage recipes. | Beverage configuration and recipe name | Saved or updated recipe confirmation, or an error message | The user has access to the recipe functionality | The recipe is stored or updated if the operation succeeds |
| FR-07 | The system shall generate personalized beverage recommendations using available user preferences, previous transactions, time of day, and weather information. | Available profile, transaction, time, and weather data | Recommended beverages and their displayed order or highlights | The recommendation functionality and relevant data are available | Recommendations are displayed using the available information |
| FR-08 | The system shall use camera-based facial-expression analysis to estimate a user's mood and adapt recommendations where this optional functionality is enabled. Facial images shall be processed in memory and discarded without being stored or transmitted. | Camera input | Estimated mood and adapted recommendations, where available | The feature is enabled and the camera is available | Recommendations are adapted without retaining or transmitting facial images |
| FR-09 | Where the optional local LLM assistant is installed and enabled, the system shall translate a user's natural-language beverage request into a proposed beverage configuration. | User's natural-language request | Proposed beverage configuration | The assistant is enabled and available | A proposed configuration is presented to the user |
| FR-10 | Where the natural-language assistant is enabled, the system shall allow users to review and modify its proposed configuration before placing an order. | Proposed configuration and user modifications | Updated configuration ready for user confirmation | A proposed configuration has been generated | The user can review and modify the configuration before ordering |
| FR-11 | The system shall support payment using the specified credit/debit cards, supported mobile wallets, and employee prepaid cards. | Beverage order and selected payment method | Payment success or failure result | The selected payment method and required payment service are available | The order's payment result is provided |
| FR-12 | The system shall provide a receipt by QR code or email after a completed transaction, according to the selected or configured delivery method. | Completed transaction and receipt-delivery information | QR code or email receipt | The transaction is completed and the relevant receipt method is available | The receipt is made available or a delivery failure is reported |
| FR-13 | The system shall record each completed transaction, including its beverage customization parameters. | Completed transaction and customization details | Transaction record | A transaction has been completed | The transaction and its customization details are recorded |
| FR-14 | The system shall restrict administrative functions to authorized maintenance personnel using a supported method, such as a physical key, master NFC card, or technician PIN. | Administrative access method | Access granted or denied | The administrative interface is available | Only authorized personnel can access administrative functions |
| FR-15 | The system shall allow authorized technicians to view ingredient levels, register refills, and reset relevant ingredient counters after refilling. | Ingredient readings and technician refill/reset actions | Updated inventory information or an error message | The technician is authorized and inventory functions are available | Inventory records reflect successful updates |
| FR-16 | The system shall monitor liquid waste and coffee grounds capacity, alert technicians when disposal is needed, and halt operation if an overflow condition occurs. | Waste-level readings and configured thresholds | Waste status, technician alerts, and a halt signal when overflow occurs | Waste monitoring is available and thresholds are configured | The technician is alerted when required, and operation halts when overflow is detected |
| FR-17 | The system shall display errors on the administrative dashboard and record events in logs to support diagnostics. | System errors and events | Dashboard messages and event-log entries | The monitoring and logging functions are available | Relevant errors and events are made available for diagnosis |
| FR-18 | When network connections or external services fail, the system shall provide basic manual ordering and any supported fallback payment handling. | Manual order and available fallback-service status | Manual-order interface and the result of any supported fallback payment handling | A network or external-service failure occurs | Supported fallback functions remain available; the exact offline-payment behavior requires confirmation |

## 2. Non-Functional Requirements and Constraints

| ID | Description | Basis or clarification needed |
|---|---|---|
| NFR-01 — Privacy | Facial images shall be processed in memory and discarded without being stored or transmitted. | Explicitly stated in the system description |
| NFR-02 — Administrative Security | Administrative functions shall be accessible only to authorized maintenance personnel. | Explicitly stated; the supported authorization methods are described in FR-14 |
| NFR-03 — Reliability | The system shall provide the specified basic manual-ordering fallback when network connections or external services fail. | Explicitly stated; exact fallback and payment behavior require confirmation |
| NFR-04 — Data Integrity | Recorded transaction details shall correspond to the completed transaction and its customization parameters. | Proposed quality constraint based on transaction recording; validation rules need confirmation |
| NFR-05 — Interactive Performance | Menu customization and recommendation displays shall respond quickly enough to support interactive use. | Qualitative proposal; measurable response-time targets are unspecified |
| NFR-06 — Personal Data Protection | Account information, preferences, and transaction records shall be protected against unauthorized access. | Reasonable security constraint; specific mechanisms and retention rules are unspecified |
| NFR-07 — Local Assistant Deployment | The optional LLM assistant shall operate locally on the machine's embedded computing module when that feature is provided. | Architectural constraint from the system description; applies only to deployments that include the assistant |

## 3. Unresolved Questions and Assumptions

1. What payment methods, if any, can continue to operate during a network outage?
2. Who configures ingredient and waste thresholds, and how are sensor readings validated?
3. How are recommendation scores calculated, and what happens when weather data is unavailable?
4. Is mood detection optional for the user, and can the user decline camera-based analysis?
5. What should happen when the optional LLM assistant is unavailable or misunderstands a request?
6. What response-time targets should apply to interactive features?
7. How long are transaction records retained, and who can access them?
8. What should the system do if receipt delivery, a camera, or a waste-level sensor fails?

These requirements are a reviewed proposal rather than a claim that every detail has been approved by stakeholders. Unspecified behavior remains open for confirmation.