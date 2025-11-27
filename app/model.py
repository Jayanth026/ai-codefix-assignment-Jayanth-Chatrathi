import os
import json
import difflib
import time
from openai import OpenAI


class CodeFixModel:
    def __init__(self):
        """
        Use OpenAI gpt-4o-mini via the new OpenAI client.
        Requires OPENAI_API_KEY to be set in the environment.
        """
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"[Model] Using OpenAI model: {self.model_name}")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set in environment")

        self.client = OpenAI(api_key=api_key)

    def _build_prompt(self, vuln_type: str, code: str) -> str:
        return f"""
You are a security code-fixing assistant.

You will be given vulnerable source code and the type of vulnerability.

Your task is:
1. Securely fix ONLY the vulnerable parts of the code.
2. Briefly explain why it was vulnerable and how you fixed it.
3. Provide a unified diff between original and fixed code.

### Requirements:
- Return STRICT JSON ONLY
- Never include markdown, backticks, comments, or explanation outside JSON
- JSON must contain exactly these fields:

{{
  "fixed_code": "<secure code>",
  "explanation": "<why it was vulnerable and how fixed>",
  "diff": "<unified diff of changes>"
}}

### Rules:
- Do NOT rewrite unrelated code
- Only fix what is necessary
- diff must follow unified diff format (`---`, `+++`, `@@`)
- JSON output must be valid, must not contain trailing commas

### Vulnerability type:
{vuln_type}

### Original code:
```code
{code}
```"""

    def _extract_json(self, text: str) -> dict:
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            cleaned = text[start:end]
            return json.loads(cleaned)
        except Exception as e:
            print(f"[Model] JSON parsing failed: {e}")
            return {
                "fixed_code": "// No fix produced.",
                "explanation": "",
                "diff": ""
            }

    def _make_diff(self, old: str, new: str) -> str:
        diff = difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile="vulnerable",
            tofile="fixed",
            lineterm=""
        )
        diff_str = "\n".join(diff)
        return diff_str or "(no differences)"

    def generate_fix(self, vuln_type: str, code: str):
        """
        Call OpenAI to fix the code and return:
        - fixed_code
        - explanation
        - diff
        - model_name
        - input_tokens
        - output_tokens
        """
        prompt = self._build_prompt(vuln_type, code)

        start = time.time()
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior application security engineer who fixes "
                        "vulnerabilities in code and responds ONLY with JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )
        _latency_ms_model = (time.time() - start) * 1000.0  # not returned, only for debugging

        message = response.choices[0].message
        output_text = message.content

        usage = getattr(response, "usage", None)
        input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
        output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0

        # Extract JSON
        result = self._extract_json(output_text)

        fixed_code = result.get("fixed_code", "").strip()
        explanation = result.get("explanation", "").strip()
        diff = result.get("diff", "").strip()

        if not fixed_code:
            fixed_code = "// No fix produced."

        # If model did not produce a proper diff, generate one locally
        if not diff or diff == "(no differences)":
            diff = self._make_diff(code, fixed_code)

        return fixed_code, explanation, diff, self.model_name, input_tokens, output_tokens
