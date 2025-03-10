## Mongo Assistant - Smart Aggregation Query Builder

### User Insight
_Describe the insight or information you are looking for from the database._

---

### Step 1: Auto-Detect Database and Collection(s)
- The assistant will infer the relevant database and collection(s) based on your insight.
- If multiple collections seem relevant, it will prompt for clarification.

---

### Step 2: Infer and Analyze Fields
_The assistant will inspect the structure of the selected collection(s) and determine key fields._

- It will automatically identify important fields for aggregation.
- If additional filtering or specific fields are required, it will ask for clarification.

---

### Step 3: Construct Aggregation Logic
- The assistant will determine the best way to group, filter, and process the data.
- It will suggest operations like `grouping`, `counting`, `summing`, or `averaging`.
- If a specific operation is ambiguous, it will prompt the user for clarification.

---

### Step 4: Explain the Query Before Execution
_The assistant will describe its understanding of the aggregation query in plain English._

- The explanation will include:
  - What data is being analyzed
  - How it is being grouped or filtered
  - Any calculations being performed
- The user can review and modify before execution.

---

### Step 5: Execute and Refine
- The query will be executed, and results will be displayed.
- If adjustments are needed, the assistant will refine the query iteratively based on user feedback.

_This streamlined process ensures minimal user involvement unless necessary while maintaining clarity on what is being queried._

