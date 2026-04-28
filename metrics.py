
import pandas as pd
def run_metrics(state):
    df = state["df"]

    sensitive = state["schema"]["sensitive"]
    target = state["schema"]["target"]

    # -----------------------------------------
    # VALIDATION
    # -----------------------------------------
    if sensitive not in df.columns:
        return {**state, "error": "Sensitive column not found."}

    if target not in df.columns:
        return {**state, "error": "Target column not found."}

    # -----------------------------------------
    # CLEAN TARGET
    # -----------------------------------------
    df[target] = df[target].replace({
    "yes":1, "no":0,
    "approved":1, "rejected":0,
    "true":1, "false":0
})
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df = df.dropna(subset=[target])

    groups = df[sensitive].dropna().unique().tolist()

    if len(groups) < 2:
        return {**state, "error": "Need at least 2 groups."}

    # -----------------------------------------
    # CALCULATE RATE FOR EACH GROUP
    # -----------------------------------------
    rates = {}
    counts = {}

    for g in groups:
        sub = df[df[sensitive] == g]

        rates[g] = float(sub[target].mean())
        counts[g] = int(len(sub))

    # -----------------------------------------
    # BEST GROUP vs WORST GROUP
    # -----------------------------------------
    max_group = max(rates, key=rates.get)
    min_group = min(rates, key=rates.get)

    rate1 = rates[max_group]
    rate2 = rates[min_group]

    gap = abs(rate1 - rate2)

    # -----------------------------------------
    # REPRESENTATION GAP
    # -----------------------------------------
    total = len(df)

    proportions = {}
    for g in groups:
        proportions[g] = counts[g] / total

    rep_gap = max(proportions.values()) - min(proportions.values())

    # -----------------------------------------
    # FAIRNESS SCORE
    # -----------------------------------------
    score = 100

    score -= gap * 60
    score -= rep_gap * 20

    if score < 0:
        score = 0

    fairness_score = round(score, 1)

    # -----------------------------------------
    # RISK LEVEL
    # -----------------------------------------
    if fairness_score >= 80:
        risk = "Low"
    elif fairness_score >= 55:
        risk = "Medium"
    else:
        risk = "High"

    # -----------------------------------------
    # FINAL BIAS FLAG
    # -----------------------------------------
    biased = gap >= 0.20

    # -----------------------------------------
    # RETURN
    # -----------------------------------------
    return {
        **state,
        "metrics": {

            # Compared groups
            "group1": str(max_group),
            "group2": str(min_group),

            # Main rates
            "rate1": round(rate1, 3),
            "rate2": round(rate2, 3),

            # Main gap
            "gap": round(gap, 3),

            # All group data
            "all_group_rates": rates,
            "group_counts": counts,

            # Representation
            "representation_gap": round(rep_gap, 3),

            # Final score
            "fairness_score": fairness_score,
            "risk_level": risk,
            "biased": bool(biased)
        }
    }
def diagnose_bias_drivers(df, sensitive, target):
    drivers = []

    ignore = [sensitive, target]

    for col in df.columns:
        if col in ignore:
            continue

        try:
            # numeric column
            if pd.api.types.is_numeric_dtype(df[col]):
                grp = df.groupby(sensitive)[col].mean()

                if len(grp) >= 2:
                    diff = grp.max() - grp.min()

                    if diff != 0:
                        drivers.append(
                            f"{col}: average differs across groups "
                            f"({round(diff,2)})"
                        )

            # categorical column
            else:
                tab = pd.crosstab(df[sensitive], df[col], normalize="index")

                if len(tab.index) >= 2:
                    spread = (tab.max() - tab.min()).max()

                    if spread > 0.15:
                        drivers.append(
                            f"{col}: category distribution varies by group"
                        )

        except:
            pass

    return drivers[:5]