# ai-codefix-assignment-Jayanth-Chatrathi

This project implements a local FastAPI service that uses OpenAI's `gpt-4o-mini` model to analyze insecure code, explain the vulnerability, and generate a fixed version. It includes a benchmarking script (`test_local.py`) that measures latency, token usage, and output quality.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Jayanth026/ai-codefix-assignment-Jayanth-Chatrathi.git
cd ai-codefix-assignment
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API Key
**Windows (PowerShell):**
```powershell
setx OPENAI_API_KEY "your-key-here"
```

**Mac/Linux (bash/zsh):**
```bash
export OPENAI_API_KEY="your-key-here"
```

### 4. Run the FastAPI Server
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🤖 How the Model Was Run

The model is invoked through the `/local_fix` API route using:
- OpenAI official SDK (`client.chat.completions.create`)
- Model: **gpt-4o-mini**
- Structured system prompt for code vulnerability remediation
- Strict JSON parsing
- Response includes diff, explanation, fixed code, token usage, and latency

---

## Example Input & Output

### **Request (SQL Injection Java)**

```json
{
  "vulnerability_type": "sql_injection",
  "language": "java",
  "cwe": "CWE-89",
  "code": "String query = "SELECT * FROM users WHERE id=" + userId;"
}
```

### **Output (summary)**

```
Explanation:
The original code was vulnerable to SQL Injection...

Diff:
--- original_code.java
+++ fixed_code.java
-String query = "SELECT * FROM users WHERE id=" + userId;
+String query = "SELECT * FROM users WHERE id=?";
+PreparedStatement pstmt = connection.prepareStatement(query);
+pstmt.setInt(1, userId);

Fixed code:
String query = "SELECT * FROM users WHERE id=?";
...
```

---

## Observations About Performance

| Test Case | Model Latency | Output Tokens |
|----------|---------------|---------------|
| SQL Injection | ~5.0 sec | 181 |
| Hardcoded Secret | ~4.8 sec | 158 |
| XSS JavaScript | ~4.0 sec | 163 |

### **General Performance Notes**
- Response time consistently between **4–6 seconds** per request.
- Token usage is efficient (<450 total tokens/request).
- Model produces high-quality secure code patches.
- Zero failures after final fixes (JSON schema + message parsing corrected).

---

## Assumptions & Limitations

### Assumptions
- Input code is short (a few lines).
- Each vulnerability corresponds to a single remediation.
- Model always returns consistent JSON structure.

### Limitations
- Not a full static analysis engine (LLM‑based only).
- Diff accuracy may vary for large files.
- Does not execute the code to confirm correctness.
- Limited to the patterns defined in the system prompt.
- No multi-file or project‑wide analysis.

