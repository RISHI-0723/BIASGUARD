import pandas as pd
import json

from metrics import run_metrics as calc_metrics
from metrics import diagnose_bias_drivers
from llm import get_llm

llm = get_llm()


# =====================================================
# 1. LOAD DATASET
# =====================================================
def load_dataset(state):
    df = pd.read_csv(state["file"])

    return {
        **state,
        "df": df,
        "columns": df.columns.tolist()
    }


# =====================================================
# 2. DETECT SCHEMA (AI-FIRST)
# =====================================================
def detect_schema(state):
    df = state["df"]
    cols = list(df.columns)

    def clean(x):
        return str(x).strip().lower()

    def is_id(col):
        c = clean(col)
        return (
            c == "id"
            or c.endswith("_id")
            or "uuid" in c
            or "guid" in c
        )

    usable_cols = [c for c in cols if not is_id(c)]

    sample_rows = df.head(5).to_dict(orient="records")

    prompt = f"""
You are an expert AI fairness auditor.

Dataset Columns:
{usable_cols}

Sample Rows:
{sample_rows}

Task:
1. Find the most likely sensitive column.
Sensitive means group column like:
gender, age group, region, zone, college tier, category etc.

2. Find most likely target column.
Target means final outcome like:
selected, approved, hired, result, status, flag etc.

3. Give confidence score (0 to 1)

Rules:
- Never choose ID columns
- Use column names + sample values
- Return only JSON

Format:
{{
  "sensitive": "...",
  "target": "...",
  "confidence": 0.0
}}
"""

    sensitive = None
    target = None
    confidence = 0.50

    try:
        res = llm.invoke(prompt)
        txt = res.content.strip()

        txt = txt.replace("```json", "").replace("```", "").strip()

        data = json.loads(txt)

        sensitive = data.get("sensitive")
        target = data.get("target")
        confidence = float(data.get("confidence", 0.50))

    except:
        pass

    # ---------------------------
    # SAFETY CHECKS
    # ---------------------------
    if sensitive not in cols:
        sensitive = None

    if target not in cols:
        target = None

    # ---------------------------
    # FALLBACK SENSITIVE
    # ---------------------------
    if sensitive is None:

        for col in usable_cols:
            uniq = df[col].nunique()

            if 2 <= uniq <= 10:
                sensitive = col
                break

    # ---------------------------
    # FALLBACK TARGET
    # ---------------------------
    if target is None:

        for col in usable_cols:
            uniq = df[col].dropna().nunique()

            if uniq == 2:
                target = col
                break

    if sensitive is None:
        sensitive = usable_cols[0]

    if target is None:
        target = usable_cols[-1]

    # avoid same column
    if sensitive == target:
        for col in usable_cols:
            if col != target:
                sensitive = col
                break

    return {
        **state,
        "schema": {
            "sensitive": sensitive,
            "target": target,
            "confidence": round(confidence, 2)
        }
    }


# =====================================================
# 3. VALIDATE SCHEMA
# =====================================================
def validate_schema(state):
    schema = state["schema"]

    if not schema["sensitive"] or not schema["target"]:
        state["error"] = "Could not detect dataset structure."

    return state


# =====================================================
# 4. RUN METRICS
# =====================================================
def run_metrics(state):
    if "error" in state:
        return state

    return calc_metrics(state)
def diagnose_results(state):
    if "error" in state:
        return state

    df = state["df"]
    sensitive = state["schema"]["sensitive"]
    target = state["schema"]["target"]

    state["bias_diagnostics"] = diagnose_bias_drivers(
        df, sensitive, target
    )

    return state


# =====================================================
# 5. EXPLAIN RESULTS
# =====================================================
def explain_results(state):
    if "metrics" not in state:
        return state

    prompt = f"""
You are an enterprise fairness auditor.

Metrics:
{state["metrics"]}

Possible Drivers:
{state.get("bias_diagnostics", [])}

Write:
1. One-line verdict
2. What the disparity means
3. Risk level insight

Keep it concise, clear, professional.
"""

    res = llm.invoke(prompt)

    state["summary"] = res.content
    return state


# =====================================================
# 6. RECOMMEND ACTIONS
# =====================================================
def recommend_actions(state):
    if "metrics" not in state:
        return state

    prompt = f"""
Given these fairness metrics:

{state["metrics"]}

Give 4 short practical recommendations for an organization.
Use bullet points.
"""

    res = llm.invoke(prompt)

    state["recommendations"] = res.content
    return state


# =====================================================
# 7. BUILD REPORT
# =====================================================
def build_report(state):
    if "metrics" not in state:
        return state

    report = f"""
BiasGuard AI Report
==============================

Sensitive Column : {state["schema"]["sensitive"]}
Decision Column  : {state["schema"]["target"]}
Confidence Score : {state["schema"]["confidence"]}

Metrics:
{state["metrics"]}

Summary:
{state["summary"]}

Recommendations:
{state["recommendations"]}
"""

    state["report"] = report
    return state