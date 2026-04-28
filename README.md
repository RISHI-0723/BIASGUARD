# 🛡️ BiasGuard AI

> **BiasGuard AI** is an intelligent fairness auditing platform that detects hidden bias in decision-making datasets such as hiring, college admissions, loan approvals, and promotions.  
It combines **statistical fairness metrics + AI explainability + workflow automation** to help organizations make more transparent and ethical decisions.

---

## 🚀 Problem Statement

Many organizations use datasets and automated systems to make decisions.  
These decisions may unintentionally favor one group over another based on factors like:

- Gender
- College Tier
- Region
- Experience
- Category / Social Groups
- Other demographic attributes

BiasGuard AI helps identify these risks early.

---

## ✨ Key Features

### 📂 Smart Dataset Upload
Upload any CSV dataset containing decision outcomes.

### 🧠 Automatic Schema Detection
Uses AI + rule logic to identify:

- Sensitive Column (Gender, Tier, Region, etc.)
- Target Column (Selected, Approved, Hired, etc.)

### 📊 Fairness Metrics Engine
Calculates:

- Selection Rate Gap
- Representation Gap
- Fairness Score (0–100)
- Risk Level (Low / Medium / High)

### 🔍 Bias Driver Analysis
Checks all columns and identifies likely causes of disparity.

Example:

- CGPA differences
- Tier 1 concentration
- Experience imbalance
- Regional skew

### 💬 AI Insight Generator
Converts raw metrics into easy-to-understand natural language insights.

### ✅ Corrective Recommendations
Provides governance and fairness improvement suggestions.

### 📄 Executive Report
Final decision-ready summary for HR / management / institutions.

---

## 🧠 Tech Stack

| Category | Technology |
|--------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Data Processing | Pandas, NumPy |
| Workflow Engine | LangGraph |
| LLM Integration | Groq (Llama 3.3 70B) |
| Semantic Search | FAISS |
| Embeddings | Sentence Transformers |
| Visualization | Streamlit Charts |

---

## ⚙️ System Workflow

```text
Upload CSV
↓
Load Dataset
↓
Detect Schema
↓
Validate Inputs
↓
Compute Fairness Metrics
↓
Diagnose Bias Drivers
↓
Generate AI Insights
↓
Recommend Actions
↓
Dashboard + Report
