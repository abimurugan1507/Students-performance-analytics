
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. CUSTOM DESIGN
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7ff, #eef8ff);
    }

    .hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, #312e81, #6366f1, #06b6d4);
        color: white;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 6px;
    }

    .hero p {
        color: #eef2ff;
        font-size: 15px;
        margin-bottom: 0;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dbeafe;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    section[data-testid="stSidebar"] {
        background-color: #eef2ff;
    }

    .insight {
        background: white;
        border: 1px solid #dbeafe;
        border-left: 5px solid #6366f1;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    .small-note {
        color: #64748b;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# 3. LOAD DATA
# ==================================================

file_path = Path(__file__).parent / "student_data.csv"

st.markdown(
    """
    <div class="hero">
        <h1>🎓 Student Performance Analytics</h1>
        <p>
        Discover academic patterns, compare student groups,
        explore grade relationships, and generate data-driven insights.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if not file_path.exists():
    st.error("student_data.csv was not found in the app.py folder.")
    st.info(f"Expected location: {file_path}")
    st.stop()

try:
    df = pd.read_csv(file_path)
except Exception as error:
    st.error(f"Could not read the CSV file: {error}")
    st.stop()

df.columns = df.columns.str.strip()

if df.empty:
    st.error("Your dataset is empty.")
    st.stop()

required_columns = ["G1", "G2", "G3"]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(f"Required columns missing: {missing_columns}")
    st.stop()

# Convert numeric columns safely
numeric_candidates = [
    "age", "studytime", "traveltime", "failures",
    "absences", "G1", "G2", "G3", "Medu", "Fedu",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health"
]

for col in numeric_candidates:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["G1", "G2", "G3"]).copy()

if df.empty:
    st.error("No valid student grade records were found.")
    st.stop()

# ==================================================
# 4. SIDEBAR FILTERS
# ==================================================

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Select categories to update the analysis.")

filtered = df.copy()

filter_columns = [
    "school", "sex", "address", "studytime",
    "guardian", "famsize"
]

for col in filter_columns:
    if col in filtered.columns:
        options = sorted(
            filtered[col].dropna().unique().tolist(),
            key=str
        )

        if options:
            selected = st.sidebar.multiselect(
                f"{col.title()}",
                options=options,
                default=options,
                key=f"filter_{col}"
            )

            if selected:
                filtered = filtered[filtered[col].isin(selected)]
            else:
                filtered = filtered.iloc[0:0]

if filtered.empty:
    st.warning("No records match these filters. Change the sidebar selections.")
    st.stop()

if "G3" in filtered.columns:
    grade_min = float(filtered["G3"].min())
    grade_max = float(filtered["G3"].max())

    if grade_min < grade_max:
        grade_range = st.sidebar.slider(
            "Final Grade Range",
            min_value=grade_min,
            max_value=grade_max,
            value=(grade_min, grade_max),
            step=1.0
        )

        filtered = filtered[
            filtered["G3"].between(
                grade_range[0], grade_range[1]
            )
        ]

if filtered.empty:
    st.warning("No students remain in the selected grade range.")
    st.stop()

st.sidebar.divider()
st.sidebar.caption("Dataset: student_data.csv")
st.sidebar.caption(f"Original records: {len(df)}")

# ==================================================
# 5. KPI CARDS
# ==================================================

total_students = len(filtered)
average_grade = filtered["G3"].mean()
highest_grade = filtered["G3"].max()
low_score_count = int((filtered["G3"] <= 10).sum())
low_score_percent = low_score_count / total_students * 100

st.subheader("📌 Performance at a Glance")

k1, k2, k3, k4 = st.columns(4)

k1.metric("👨‍🎓 Total Students", f"{total_students:,}")
k2.metric("📈 Average Final Grade", f"{average_grade:.2f} / 20")
k3.metric("🏆 Highest Grade", f"{highest_grade:g} / 20")
k4.metric(
    "⚠️ Grade ≤ 10",
    f"{low_score_count}",
    delta=f"{low_score_percent:.1f}% of students",
    delta_color="off"
)

st.caption(
    "All metrics update according to your selected filters."
)

st.divider()

# ==================================================
# 6. GRADE CATEGORY DISTRIBUTION
# ==================================================

st.subheader("📊 Final Grade Distribution")

def grade_category(grade):
    if grade <= 5:
        return "Needs Improvement (0–5)"
    elif grade <= 10:
        return "Average (6–10)"
    elif grade <= 15:
        return "Good (11–15)"
    return "Excellent (16–20)"

category_order = [
    "Needs Improvement (0–5)",
    "Average (6–10)",
    "Good (11–15)",
    "Excellent (16–20)"
]

category_colors = [
    "#ef4444", "#f59e0b", "#3b82f6", "#10b981"
]

grade_data = filtered.copy()
grade_data["Grade Category"] = grade_data["G3"].apply(
    grade_category
)

category_counts = (
    grade_data["Grade Category"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

category_percentages = (
    category_counts / total_students * 100
)

left, right = st.columns(2)

with left:
    fig, ax = plt.subplots(figsize=(8, 5))

    nonzero = category_counts[category_counts > 0]

    if len(nonzero) > 0:
        color_lookup = dict(zip(category_order, category_colors))

        ax.pie(
            nonzero.values,
            labels=nonzero.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=[color_lookup[label] for label in nonzero.index],
            wedgeprops={"edgecolor": "white", "linewidth": 2}
        )
        ax.set_title("Share of Students by Grade Category")
    else:
        ax.text(0.5, 0.5, "No grade data", ha="center", va="center")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.markdown("#### Grade Category Summary")

    category_table = pd.DataFrame({
        "Grade Category": category_order,
        "Student Count": category_counts.values,
        "Percentage (%)": category_percentages.values
    })

    st.dataframe(
        category_table.style.format({
            "Percentage (%)": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    fig, ax = plt.subplots(figsize=(8, 3.8))

    ax.barh(
        category_order,
        category_percentages.values,
        color=category_colors
    )

    ax.set_xlabel("Students (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Percentage by Category")
    ax.grid(axis="x", alpha=0.2)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# ==================================================
# 7. GRADE PROGRESSION
# ==================================================

st.subheader("📚 Grade Progression")

grade_means = filtered[["G1", "G2", "G3"]].mean()

progress_col1, progress_col2 = st.columns([1, 2])

with progress_col1:
    st.markdown("#### Average Grades")

    for grade_name, grade_value in grade_means.items():
        st.metric(
            label=f"{grade_name} Average",
            value=f"{grade_value:.2f} / 20"
        )

    change = grade_means["G3"] - grade_means["G1"]

    st.metric(
        "G1 to G3 Difference",
        f"{change:+.2f} points",
        delta_color="normal"
    )

with progress_col2:
    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(
        ["G1", "G2", "G3"],
        grade_means.values,
        marker="o",
        markersize=9,
        linewidth=3,
        color="#6366f1"
    )

    ax.set_ylim(0, 20)
    ax.set_ylabel("Average Grade")
    ax.set_title("Average Grade Across Three Periods")
    ax.grid(alpha=0.25)

    for x, y in zip(["G1", "G2", "G3"], grade_means.values):
        ax.annotate(
            f"{y:.2f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center"
        )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.caption(
    "G1, G2 and G3 are grades from three periods. "
    "This chart compares their averages; it does not show individual student trajectories."
)

st.divider()

# ==================================================
# 8. CORRELATION HEATMAP
# ==================================================

st.subheader("🔗 Correlation Analysis")

correlation_columns = [
    col for col in ["G1", "G2", "G3", "studytime", "absences"]
    if col in filtered.columns
]

if len(correlation_columns) >= 2:
    correlation_matrix = filtered[
        correlation_columns
    ].corr(numeric_only=True)

    fig, ax = plt.subplots(
        figsize=(8, max(4, len(correlation_columns) * 1.0))
    )

    matrix_values = correlation_matrix.values

    image = ax.imshow(
        matrix_values,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        aspect="auto"
    )

    ax.set_xticks(range(len(correlation_columns)))
    ax.set_xticklabels(correlation_columns)
    ax.set_yticks(range(len(correlation_columns)))
    ax.set_yticklabels(correlation_columns)

    for i in range(len(correlation_columns)):
        for j in range(len(correlation_columns)):
            value = matrix_values[i, j]

            ax.text(
                j, i, f"{value:.2f}",
                ha="center",
                va="center",
                color="black",
                fontsize=10
            )

    ax.set_title("Pearson Correlation Heatmap")
    fig.colorbar(image, ax=ax, label="Correlation (-1 to +1)")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("#### Relationship with Final Grade (G3)")

    if "G3" in correlation_matrix.columns:
        g3_correlations = (
            correlation_matrix["G3"]
            .drop(labels=["G3"], errors="ignore")
            .sort_values(key=lambda values: values.abs(), ascending=False)
        )

        st.dataframe(
            g3_correlations.rename(
                "Correlation with G3"
            ).reset_index().rename(
                columns={"index": "Variable"}
            ).style.format({
                "Correlation with G3": "{:.3f}"
            }),
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Pearson correlation measures linear association. "
        "Correlation does not establish causation."
    )
else:
    st.info("Not enough numeric columns for correlation analysis.")

st.divider()

# ==================================================
# 9. STUDY TIME ANALYSIS
# ==================================================

st.subheader("⏱️ Study Time and Final Grades")

if "studytime" in filtered.columns:
    study_summary = (
        filtered.dropna(subset=["studytime"])
        .groupby("studytime", observed=True)["G3"]
        .agg(["count", "mean", "max"])
        .reset_index()
    )

    if not study_summary.empty:
        a, b = st.columns([1, 1])

        with a:
            st.markdown("#### Average Grade by Study Time")

            fig, ax = plt.subplots(figsize=(7, 4.5))

            ax.bar(
                study_summary["studytime"].astype(str),
                study_summary["mean"],
                color="#8b5cf6"
            )

            ax.set_xlabel("Study Time Category")
            ax.set_ylabel("Average Final Grade")
            ax.set_ylim(0, 20)
            ax.grid(axis="y", alpha=0.2)

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with b:
            st.markdown("#### Study Time Summary")

            study_display = study_summary.rename(
                columns={
                    "studytime": "Study Time",
                    "count": "Student Count",
                    "mean": "Average Grade",
                    "max": "Highest Grade"
                }
            )

            st.dataframe(
                study_display.style.format({
                    "Average Grade": "{:.2f}",
                    "Highest Grade": "{:.0f}"
                }),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "In this dataset, studytime is a category code: "
                "1 means less study time and 4 means the highest category."
            )
else:
    st.info("No studytime column is available.")

st.divider()

# ==================================================
# 10. ABSENCES ANALYSIS
# ==================================================

st.subheader("📅 Absences and Academic Performance")

if "absences" in filtered.columns:
    abs_data = filtered.dropna(subset=["absences", "G3"]).copy()

    if not abs_data.empty:
        abs_data["Absence Category"] = pd.cut(
            abs_data["absences"],
            bins=[-1, 0, 5, 10, float("inf")],
            labels=[
                "0 absences",
                "1–5",
                "6–10",
                "Above 10"
            ]
        )

        abs_summary = (
            abs_data.groupby(
                "Absence Category",
                observed=False
            )["G3"]
            .agg(["count", "mean"])
            .reset_index()
        )

        a, b = st.columns(2)

        with a:
            fig, ax = plt.subplots(figsize=(7, 4.5))

            ax.scatter(
                abs_data["absences"],
                abs_data["G3"],
                alpha=0.65,
                color="#f97316"
            )

            ax.set_xlabel("Number of Absences")
            ax.set_ylabel("Final Grade (G3)")
            ax.set_title("Absences vs Final Grade")
            ax.set_ylim(-1, 21)
            ax.grid(alpha=0.2)

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with b:
            st.markdown("#### Average Grade by Absence Group")

            abs_display = abs_summary.rename(
                columns={
                    "Absence Category": "Absence Group",
                    "count": "Student Count",
                    "mean": "Average Grade"
                }
            )

            st.dataframe(
                abs_display.style.format({
                    "Average Grade": "{:.2f}"
                }),
                use_container_width=True,
                hide_index=True
            )

        st.caption(
            "These are observed associations. Other factors may also affect grades."
        )
else:
    st.info("No absences column is available.")

st.divider()

# ==================================================
# 11. AUTOMATIC INSIGHTS
# ==================================================

st.subheader("💡 Key Data Insights")

insights = []

insights.append(
    f"The average final grade for the selected students is "
    f"{average_grade:.2f} out of 20."
)

insights.append(
    f"{low_score_count} students ({low_score_percent:.1f}%) "
    f"scored 10 or below."
)

top_category = category_counts.idxmax()
top_category_percent = category_percentages.loc[top_category]

insights.append(
    f"The largest grade category is {top_category}, "
    f"representing {top_category_percent:.1f}% of selected students."
)

if "studytime" in filtered.columns:
    study_valid = filtered.dropna(subset=["studytime"])

    if not study_valid.empty:
        study_means = study_valid.groupby("studytime")["G3"].mean()

        highest_study_category = study_means.idxmax()
        highest_study_grade = study_means.max()

        insights.append(
            f"Study-time category {highest_study_category} has the "
            f"highest observed average grade ({highest_study_grade:.2f}) "
            f"among the selected study-time categories."
        )

if "G3" in correlation_matrix.columns if "correlation_matrix" in locals() else False:
    grade_corr = correlation_matrix["G3"].drop(
        labels=["G3"], errors="ignore"
    )

    if not grade_corr.empty:
        strongest_variable = grade_corr.abs().idxmax()
        strongest_value = grade_corr.loc[strongest_variable]

        insights.append(
            f"{strongest_variable} has the strongest absolute linear "
            f"correlation with G3 among the displayed variables "
            f"({strongest_value:.3f}). This is an association, not proof of causation."
        )

for index, insight in enumerate(insights, start=1):
    st.markdown(
        f"""
        <div class="insight">
            <b>Insight {index}</b><br>
            {insight}
        </div>
        """,
        unsafe_allow_html=True
    )

st.info(
    "Recommendations: investigate the students who score 10 or below, "
    "compare patterns across groups, and discuss possible explanations "
    "with additional evidence before making decisions."
)

st.divider()

# ==================================================
# 12. SEARCH AND DOWNLOAD DATA
# ==================================================

st.subheader("🔎 Explore Student Records")

search_text = st.text_input(
    "Search across visible columns",
    placeholder="Type a value such as GP, F, 17, or 10..."
)

display_df = filtered.copy()

if search_text.strip():
    search_mask = display_df.astype(str).apply(
        lambda column: column.str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False
        )
    ).any(axis=1)

    display_df = display_df[search_mask]

st.caption(
    f"Showing {len(display_df)} records out of {len(filtered)} filtered students."
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

csv_bytes = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_bytes,
    file_name="student_performance_filtered.csv",
    mime="text/csv"
)

# ==================================================
# 13. FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:15px;">
        🎓 Student Performance Analytics Dashboard<br>
        Built with Python • Pandas • Matplotlib • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
