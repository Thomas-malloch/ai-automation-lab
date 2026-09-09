AI Automation Systems Lab
1. Project Vision
Build a portfolio of production-style AI automation systems for developer and business workflows.
The goal is not to build a collection of simple LLM wrappers. Each project should demonstrate a complete automation loop:
Observe → Understand → Decide → Act → Verify
Each system should combine AI with normal software engineering components such as:
APIs
databases
queues
schedulers
browser automation
validation
structured outputs
testing
logging
retries
audit trails
human approval
dashboards
observability
The portfolio should demonstrate that AI is being used as one component inside a reliable software system rather than being treated as the entire application.

2. Overall Portfolio Structure
Repository name:
ai-automation-lab

Recommended structure:
ai-automation-lab/
│
├── README.md
├── docs/
│   ├── architecture.md
│   ├── design-principles.md
│   └── screenshots/
│
├── shared/
│   ├── ai/
│   ├── schemas/
│   ├── logging/
│   ├── workflow/
│   └── utilities/
│
├── document-processing/
│
├── competitor-intelligence/
│
├── legacy-modernizer/
│
├── churn-triage/
│
└── developer-recovery-agent/

The first three projects should be treated as the main portfolio projects.
Priority:
1. Autonomous Document Processing Pipeline
2. Competitor Pricing & Inventory Intelligence Engine
3. AI Legacy Migration Refactorer
4. Customer Churn Risk Triage Pipeline
5. Developer Environment Recovery Agent

Do not attempt to build all five simultaneously.
Finish a usable MVP of one before moving to the next.

3. Shared Design Principles
Every automation should follow roughly the same lifecycle:
Input
↓
Ingestion
↓
Pre-processing
↓
AI / analysis
↓
Structured result
↓
Validation
↓
Business rules
↓
Action
↓
Verification
↓
Persistence
↓
Audit log

Each project should try to contain the following concepts where appropriate.
Structured outputs
Never rely solely on free-form LLM responses.
AI responses should map into strongly typed structures.
Example:
{
  "supplier": "Example Ltd",
  "invoiceNumber": "INV-10321",
  "invoiceDate": "2026-09-01",
  "total": 428.50,
  "currency": "NZD",
  "confidence": 0.94
}

Validate these responses before allowing downstream actions.

Human-in-the-loop controls
AI should not automatically perform high-impact actions when confidence is low.
Example states:
AUTO_APPROVED
REVIEW_REQUIRED
REJECTED
FAILED


Auditability
Every AI decision should be traceable.
Record:
workflow ID
timestamp
input
model used
model output
validation result
actions performed
confidence
errors
final result


Retry and failure handling
Workflows should explicitly support:
SUCCESS
FAILED
RETRYING
REQUIRES_REVIEW

Avoid workflows that silently fail.

Observability
Each project should expose useful operational information.
Potential metrics:
jobs processed
success rate
failure rate
average processing time
AI requests
validation failures
human reviews
retry count
estimated API cost


4. Shared Technology Stack
Avoid forcing every project into exactly the same stack, but reuse technology where sensible.
Suggested core stack:
Backend
Java
Spring Boot
Spring Web
Spring Data JPA
PostgreSQL

Use Java for workflow APIs, persistence and application logic.

AI / data services
Python
FastAPI
Pydantic
scikit-learn
LLM APIs

Python can handle:
document extraction
ML models
embeddings
NLP
AI experimentation

Frontend
React
TypeScript

Use a shared dashboard design language across projects.

Infrastructure
Potential technologies:
Docker
PostgreSQL
Redis
RabbitMQ or Kafka later if required
Playwright
GitHub Actions

Do not introduce infrastructure unless it solves an actual problem.
For early versions, PostgreSQL plus background workers is enough.

5. Project One — Autonomous Document Processing Pipeline
Goal
Build a system that converts unstructured financial documents into validated relational database records.
Example documents:
Invoices
Purchase orders
Receipts
Bank statements
Financial reports

Start with invoices only.
Expand later.

6. Document Processing MVP
The MVP should perform:
Upload invoice
↓
Store original file
↓
Extract document text
↓
Identify document type
↓
Extract invoice fields
↓
Convert fields into typed schema
↓
Validate values
↓
Assign confidence
↓
Store valid record in PostgreSQL
↓
Send uncertain records to review queue


Initial invoice schema
Example relational model:
Supplier
--------
id
name
taxNumber

Invoice
-------
id
supplierId
invoiceNumber
invoiceDate
dueDate
currency
subtotal
tax
total
status
confidence
sourceDocument

InvoiceLine
-----------
id
invoiceId
description
quantity
unitPrice
total


Validation rules
Examples:
subtotal + tax ≈ total
invoice number cannot be empty
currency must be recognised
invoice date must be valid
line totals should approximately equal invoice subtotal
supplier must exist or be created

If validation fails:
REVIEW_REQUIRED


7. Document Processing API
Possible endpoints:
POST /api/documents
GET /api/documents
GET /api/documents/{id}

GET /api/review
POST /api/review/{id}/approve
POST /api/review/{id}/reject

GET /api/invoices
GET /api/invoices/{id}

GET /api/metrics


8. Document Processing Dashboard
Build a React dashboard showing:
Overview
Documents processed
Successful extractions
Requires review
Failed
Average confidence
Average processing time

Processing queue
Example:
INV-1004
Supplier: Example Ltd
Confidence: 96%
Status: AUTO_APPROVED

Review screen
Display:
PDF preview

Extracted values

Supplier:
[ Example Ltd ]

Invoice Number:
[ INV-1004 ]

Total:
[ $428.50 ]

Confidence:
74%

Reason:
Subtotal and extracted line items differ by $15.

Buttons:
Approve
Edit and approve
Reject


9. Document Processing Stretch Features
After the MVP works:
Duplicate invoice detection
Supplier matching
OCR for scanned documents
Multiple document types
Email ingestion
Batch uploads
Confidence calibration
Source-text highlighting
Financial anomaly detection

A particularly impressive feature would be provenance.
Example:
Total: $428.50

Source:
Page 2
"TOTAL DUE NZD $428.50"

This makes the AI output auditable.

10. Project Two — Competitor Pricing & Inventory Intelligence Engine
Goal
Build an automated system that tracks competitor products, pricing, discounts and inventory over time.
The system should convert raw website observations into useful business intelligence.

11. Competitor Intelligence Workflow
Scheduled job
↓
Browser worker launches
↓
Visit configured competitor websites
↓
Extract product information
↓
Normalize data
↓
Match competitor products
↓
Store snapshot
↓
Compare against previous snapshot
↓
Detect meaningful changes
↓
Generate business summary
↓
Alert / dashboard


12. Competitor Configuration
Create something like:
Competitor
----------
id
name
baseUrl
active

TrackedPage
-----------
id
competitorId
url
category
schedule

Eventually allow users to configure competitors through the UI.
For the MVP, configure them manually.

13. Product Observation Model
Product
-------
id
canonicalName
brand
category

CompetitorProduct
-----------------
id
productId
competitorId
externalName
url

ProductObservation
------------------
id
competitorProductId
timestamp
price
originalPrice
discount
stockStatus


14. Change Detection
The system should detect events like:
PRICE_INCREASE
PRICE_DECREASE
NEW_PRODUCT
PRODUCT_REMOVED
BACK_IN_STOCK
OUT_OF_STOCK
DISCOUNT_STARTED
DISCOUNT_ENDED

Example:
Competitor: Example Electronics
Product: Wireless Headphones

Previous price:
$199

Current price:
$169

Change:
-15.1%

Detected:
9 September 2026


15. AI Role
Do not use the LLM simply to scrape websites.
Use normal extraction first when possible.
Use AI for harder reasoning tasks such as:
product matching
category classification
change summarisation
competitive analysis
business recommendations

Example:
Market Summary

Three competitors reduced prices in the wireless audio
category this week.

Average market price fell from $187 to $174.

Your current price of $199 is approximately 14% above
the observed competitor median.


16. Competitor Intelligence Dashboard
Sections:
Market overview
Tracked competitors
Tracked products
Price changes today
New products
Stock changes

Price history
Graph:
Date → Price

Show multiple competitors for the same product.
Intelligence feed
Example:
HIGH PRIORITY

Competitor A reduced Product X by 18%.

Competitor B has now matched that price.

Your price is currently $34 higher.


17. Competitor Intelligence Stretch Features
Email/Slack alerts
Market median calculations
Automatic product matching
Embeddings for product similarity
Screenshot evidence
Dynamic scraping strategies
Proxy/browser resilience
Historical trend analysis
Automatic competitor discovery
Pricing recommendations

Do not build automatic pricing modification initially.
Keep the system intelligence-focused.

18. Project Three — AI Legacy Migration Refactorer
Goal
Build an agentic software engineering tool that progressively modernizes legacy code while verifying that behaviour is preserved.
Keep the scope deliberately constrained.
Start with:
Java legacy modernization


19. Legacy Modernizer MVP Scope
Support a small collection of migrations.
For example:
JUnit 4 → JUnit 5
javax → jakarta
Java Date → java.time
deprecated API replacements
raw collections → generics
Maven dependency updates
Java language modernization

Do not initially attempt complete framework migrations.

20. Legacy Modernization Workflow
Repository provided
↓
Scan project
↓
Build dependency / project information
↓
Run baseline compilation
↓
Run baseline tests
↓
Detect migration candidates
↓
Create migration plan
↓
Select one migration
↓
Generate patch
↓
Apply patch
↓
Compile
↓
Run tests
↓
Analyse result
↓
Accept or revert
↓
Continue

The important feature is verification.
The system should never assume a generated patch is correct.

21. Migration State Machine
Example:
DISCOVERED
PLANNED
PATCH_GENERATED
PATCH_APPLIED
COMPILING
TESTING
SUCCESS
FAILED
REVERTED
REVIEW_REQUIRED


22. Safety Controls
Use git heavily.
Before applying changes:
create working branch
create checkpoint

After changes:
compile
test

If verification fails:
analyse error
attempt limited repair

After a maximum number of retries:
revert
mark for review


23. Legacy Modernizer Example Output
Migration Run #104

Repository:
legacy-orders-service

Migration:
JUnit 4 → JUnit 5

Files changed:
27

Initial tests:
184 passing

Migration attempt:
182 passing
2 failing

Detected issue:
ExpectedException rule unsupported.

Repair:
Converted rule to assertThrows.

Final result:
184 / 184 passing

Status:
SUCCESS

This is the kind of evidence that should appear in the UI and README.

24. Static Analysis
Do not rely entirely on an LLM to understand the repository.
Gather deterministic information first.
Potential inputs:
AST
imports
Maven dependencies
compiler version
test framework
package graph
deprecated API usage

Then supply relevant context to the model.
This will make the architecture considerably stronger.

25. Legacy Modernizer Dashboard
Pages:
Repositories
Migration runs
Migration plans
Patch viewer
Build output
Test results
Audit history

Potential visualisation:
184 baseline tests

      ↓ migration

182 passing
2 failing

      ↓ repair

184 passing

✓ migration accepted


26. Legacy Modernizer Stretch Features
dependency vulnerability upgrades
Spring Boot migration
automatic pull requests
migration cost estimation
code quality analysis
multi-agent review
semantic test generation
migration dependency graphs
incremental migrations

A future GitHub integration could automatically generate PRs.

27. Project Four — Customer Churn Risk Triage Pipeline
Goal
Build a system that identifies customers who may churn and automatically prioritizes them for intervention.
Separate predictive ML from LLM reasoning.

28. Churn Pipeline
Customer activity events
↓
Feature generation
↓
Churn prediction model
↓
Risk classification
↓
Signal explanation
↓
LLM-generated summary
↓
Recommended intervention
↓
Customer success queue


29. Example Features
login frequency
usage decline
support ticket count
support sentiment
payment failures
account age
feature adoption
contract renewal proximity
team activity
administrator inactivity


30. Model
Start with something interpretable.
Possible algorithms:
logistic regression
random forest
gradient boosting

Do not begin with a neural network unless there is a clear reason.
Evaluate:
precision
recall
F1
ROC-AUC
calibration

For this use case, precision and recall at the intervention threshold matter more than simply reporting accuracy.

31. Risk Output
Example:
Customer:
Acme Ltd

Risk:
HIGH

Probability:
83%

Primary signals:

Usage down 47% over 30 days
3 unresolved support tickets
Renewal in 19 days
Account administrator inactive for 12 days

Recommended action:

Customer success manager should contact the account
within 48 hours and investigate unresolved support issues.


32. Churn Dashboard
Sections:
Total customers
High risk
Medium risk
Low risk
New high-risk customers

Prioritized queue:
Customer     Risk    Probability    Main signal

Acme Ltd     HIGH       83%         Usage decline
Example Co   HIGH       79%         Support activity
Beta Ltd     MEDIUM     61%         Low adoption


33. Churn Stretch Features
SHAP explanations
customer segmentation
time-series features
automatic CRM tasks
intervention tracking
A/B testing outreach strategies
model drift detection
feedback loop from successful interventions


34. Project Five — Developer Environment Recovery Agent
Goal
Build a local developer tool that monitors development commands and detects common environment failures.
It should diagnose problems, propose fixes and optionally execute safe recovery actions.

35. Developer Recovery Workflow
Monitor process
↓
Detect failure
↓
Capture command output
↓
Gather environment context
↓
Classify problem
↓
Run safe diagnostics
↓
Generate proposed fix
↓
Request permission if required
↓
Execute fix
↓
Retry original operation
↓
Verify


36. Initial Supported Problems
Keep the MVP narrow.
Support around 5-10 predictable issues.
Examples:
port already in use
missing dependency
Docker container stopped
database unavailable
invalid environment variable
Maven dependency failure
npm dependency failure
test failure
permission issue
incorrect Java version


37. Permission System
Create explicit permission levels.
READ_ONLY

Diagnose only.
SAFE_AUTOMATION

Automatically run non-destructive diagnostic commands.
CONFIRM_BEFORE_EXECUTION

Generate fixes but ask before modifying anything.
Do not initially build unrestricted autonomous execution.

38. Example Recovery
Spring Boot failed to start.

Detected:
Port 8080 is already occupied.

Diagnostic:
PID 4821
Process: OrbStack

Suggested fixes:

1. Start application on port 8081.
2. Terminate PID 4821.

Recommended:
Use port 8081.

Apply fix? [Y/N]

After approval:
Restarting...

Application started successfully on port 8081.

Recovery successful.


39. Security Considerations
This project should explicitly treat command execution as dangerous.
Implement:
command allowlists
working-directory restrictions
timeouts
output limits
blocked destructive commands
approval requirements
audit logs

Never automatically execute arbitrary LLM-generated shell commands.
This security model can itself become an important part of the project.

40. Shared Automation Framework
After completing the first project, identify common infrastructure that can be extracted.
Do not build a framework before you have a real need for one.
Potential shared abstractions:
Workflow
WorkflowStep
WorkflowRun
AIClient
StructuredAIResponse
ValidationResult
Action
ApprovalRequest
AuditEvent
RetryPolicy

Example concept:
public interface WorkflowStep<I, O> {

    O execute(I input);

    ValidationResult validate(O output);
}

Possible workflow execution model:
Workflow
    ↓
Step
    ↓
Result
    ↓
Validation
    ↓
Next step


41. Shared Database Concepts
Potential generic tables:
workflow_runs
workflow_steps
audit_events
ai_requests
approval_requests
system_errors

Example:
workflow_runs

id
workflow_type
status
started_at
completed_at
input_reference
error_message


42. AI Provider Abstraction
Avoid coupling every project directly to one model provider.
Create something conceptually similar to:
AIClient

generate()
generateStructured()
embed()

This makes it easier to experiment with:
OpenAI
local models
other APIs
mock models in tests


43. Testing Strategy
Every project should contain meaningful automated testing.
Unit tests
Test:
validation logic
business rules
change detection
risk calculations
workflow transitions
parsers

Integration tests
Test:
API → service → database
worker → database
AI structured response → validation

AI tests
Do not test exact wording.
Test properties.
Example:
required fields exist
JSON validates against schema
confidence within 0-1
classification belongs to allowed enum

Use mock AI responses for normal automated tests.

44. Evaluation
Each project should contain measurable evaluation instead of vague claims that it "works."
Document processing:
field extraction accuracy
document success rate
review rate
processing latency

Competitor intelligence:
price extraction accuracy
product matching accuracy
change detection precision

Legacy migration:
successful migrations
compile success
tests preserved
percentage requiring human intervention

Churn:
precision
recall
F1
ROC-AUC
calibration

Developer recovery:
diagnosis accuracy
successful recovery rate
false-fix rate
average recovery steps


45. Observability
Create consistent logging.
Example event:
{
  "workflowId": "wf-18391",
  "workflow": "invoice-processing",
  "step": "validate-extraction",
  "status": "REVIEW_REQUIRED",
  "confidence": 0.71,
  "timestamp": "2026-09-09T14:00:00"
}

Eventually add an operational dashboard.
Useful information:
runs today
successful runs
failed runs
average latency
AI token usage
estimated API cost
review rate


46. GitHub Repository Presentation
The root README should explain the portfolio rather than dump implementation detail.
Suggested opening:
AI Automation Systems Lab

A collection of autonomous and semi-autonomous systems
exploring reliable AI automation across business and
developer workflows.

The projects focus on integrating AI into complete software
systems rather than building standalone LLM interfaces.

Each automation follows a common lifecycle:

Observe → Understand → Decide → Act → Verify

Then include a project table.
Project                    Domain         Status

Document Processing        Finance        Complete
Competitor Intelligence    Commerce       In Progress
Legacy Modernizer          Development    Planned
Churn Triage               SaaS           Planned
Recovery Agent             Development    Planned


47. README Requirements for Every Project
Each sub-project should have its own README containing:
Problem
Goal
Architecture
Technology stack
Workflow
AI responsibilities
Deterministic components
Database design
Safety mechanisms
Testing
Evaluation
Screenshots
Limitations
Future work

Do not hide limitations.
Explicitly discussing limitations makes the project look more technically mature.

48. Architecture Diagrams
Create a diagram for every flagship project.
Example document pipeline:
                 ┌───────────────┐
                  │    React UI   │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Spring API    │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Workflow      │
                  │ Engine        │
                  └───────┬───────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    ┌───────────────┐           ┌───────────────┐
    │ AI Extraction │           │ Validation    │
    │ Service       │           │ Engine        │
    └───────┬───────┘           └───────┬───────┘
            │                           │
            └─────────────┬─────────────┘
                          ▼
                  ┌───────────────┐
                  │ PostgreSQL    │
                  └───────────────┘


49. Development Roadmap
Phase 0 — Repository Setup
Create:
ai-automation-lab

Add:
README.md
docs/
document-processing/

Do not create empty implementations for every project.
Only document the future roadmap.

50. Phase 1 — Document Pipeline Core
Build:
Spring Boot project
PostgreSQL
Invoice schema
Document upload
Basic persistence

Goal:
A user uploads a document and the application stores it.
No AI yet.

51. Phase 2 — Document Extraction
Add:
PDF text extraction
AI extraction service
structured invoice schema
Pydantic / JSON schema validation

Goal:
PDF → valid structured invoice object


52. Phase 3 — Validation Pipeline
Add:
financial validation
confidence
workflow states
review requirement
error handling

Goal:
Reliable processing rather than merely successful extraction.

53. Phase 4 — Review UI
Build:
React dashboard
processing queue
invoice viewer
review interface

Goal:
Make the system demonstrable.

54. Phase 5 — Observability
Add:
workflow logs
metrics
processing duration
failure reasons
AI usage

At this point, project one should be considered portfolio-ready.

55. Phase 6 — Competitor Intelligence MVP
Build:
Playwright worker
competitor configuration
product extraction
PostgreSQL snapshots
scheduled jobs

Start with only 2-3 websites.

56. Phase 7 — Change Intelligence
Add:
price comparison
inventory comparison
new product detection
alerts
AI summaries
dashboard

Finish project two before moving forward.

57. Phase 8 — Legacy Modernizer MVP
Choose only one migration initially.
Best starting candidate:
JUnit 4 → JUnit 5

Implement:
repository scanning
test baseline
migration planning
patch generation
patch application
compilation
testing
rollback

Once this works reliably, add additional migrations.

58. Phase 9 — Remaining Projects
Only build churn and developer recovery after the first three projects are strong.
They can initially be smaller experiments.

59. What Not to Build Initially
Avoid adding:
Kubernetes
microservices everywhere
Kafka
complex authentication
multi-tenancy
billing
mobile applications
dozens of agents
vector databases without a clear reason
fully autonomous command execution

These can create complexity without improving the project.
Start as a modular monolith where possible.
Extract services only where there is a clear technical reason.

60. Portfolio Quality Standard
A project should not be considered complete because:
"The AI returned the correct answer once."

A project is complete when you can demonstrate:
input
processing
AI reasoning
validation
persistence
errors
retries
user interaction
testing
metrics
final outcome


61. Suggested Flagship Architecture
For the first few projects, use roughly:
React / TypeScript
        │
        ▼
Spring Boot REST API
        │
        ├──────────────► PostgreSQL
        │
        ▼
Workflow Service
        │
        ├──────────────► Background workers
        │
        ├──────────────► Python AI service
        │
        └──────────────► External tools/APIs

This is enough complexity to demonstrate real engineering without becoming unnecessarily difficult.

62. CV Strategy
Do not list the portfolio as five tiny projects.
Once enough has been built, potentially create a single entry:
AI Automation Systems Lab | Java, Spring Boot, Python, React,
PostgreSQL, Playwright

• Designed and implemented production-style AI automation
  workflows spanning document processing, competitive
  intelligence and software modernization.

• Built reliable AI pipelines using structured model outputs,
  deterministic validation, workflow state management,
  retries, audit logging and human approval controls.

• Developed an autonomous financial document pipeline that
  converted unstructured invoices into validated relational
  database records with confidence-based review routing.

• Built a browser-driven competitive intelligence engine that
  tracked pricing, inventory and product changes across
  competitor websites and generated automated market insights.

• Developed an agentic Java modernization system capable of
  generating code migrations, compiling changes, executing
  regression tests and automatically reverting failed patches.

Only make these claims once the respective features genuinely exist.

63. Success Criteria
The portfolio succeeds if it demonstrates that you understand the difference between:
AI feature

and:
AI system

The key concepts you should be able to discuss in an interview are:
When should AI be used?

When should deterministic software be used?

How do you validate AI output?

How do you prevent unsafe actions?

How do you recover from failures?

How do you measure whether the AI actually works?

How do you retain provenance?

How do you introduce human review?

How do you design workflows around uncertain components?

How do you observe and debug AI systems?

Those questions are more valuable than simply being able to say that you used an LLM API.

64. Immediate Starting Point
Start only with:
ai-automation-lab/
└── document-processing/

First milestone:
Build a backend capable of accepting an invoice PDF, storing the original document and creating a processing job.
Second milestone:
Extract text and convert the invoice into a strongly typed structure.
Third milestone:
Validate the structured result and persist valid invoice and invoice-line records.
Fourth milestone:
Route uncertain documents into a human review queue.
Fifth milestone:
Build the dashboard.
Only after those five milestones work should development begin on the competitor intelligence system.
The long-term target is not five enormous commercial products.
The target is a coherent portfolio containing approximately:
2 polished flagship systems
1 technically ambitious prototype
2 smaller experiments

That is realistic enough to finish while still being ambitious enough to become a significant CV and learning project.

