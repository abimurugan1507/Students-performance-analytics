
import pandas as pd

# Load dataset
df = pd.read_csv("student_data.csv")

print("=" * 50)
print("STUDENT PERFORMANCE DATA ANALYSIS")
print("=" * 50)

# 1. Overall grade statistics
print("\n1. OVERALL GRADE STATISTICS")
print(df[["G1", "G2", "G3"]].describe().round(2))

# 2. Average grade by study time
print("\n2. STUDY TIME VS AVERAGE FINAL GRADE")
study_analysis = df.groupby("studytime")["G3"].agg(
    ["count", "mean", "max"]
).round(2)

print(study_analysis)

# 3. Gender-wise performance
print("\n3. GENDER-WISE PERFORMANCE")
gender_analysis = df.groupby("sex")["G3"].agg(
    ["count", "mean", "max"]
).round(2)

print(gender_analysis)

# 4. Grade categories
print("\n4. FINAL GRADE CATEGORIES")
grade_categories = pd.cut(
    df["G3"],
    bins=[-1, 5, 10, 15, 20],
    labels=[
        "Needs Improvement (0-5)",
        "Average (6-10)",
        "Good (11-15)",
        "Excellent (16-20)"
    ]
)

print(grade_categories.value_counts().reindex(
    [
        "Needs Improvement (0-5)",
        "Average (6-10)",
        "Good (11-15)",
        "Excellent (16-20)"
    ],
    fill_value=0
))

# 5. Absences vs final grade
print("\n5. ABSENCES VS AVERAGE FINAL GRADE")

df["absence_category"] = pd.cut(
    df["absences"],
    bins=[-1, 0, 5, 10, float("inf")],
    labels=["0 absences", "1-5", "6-10", "Above 10"]
)

absence_analysis = df.groupby(
    "absence_category", observed=False
)["G3"].agg(["count", "mean"]).round(2)

print(absence_analysis)

# 6. Grade progression
print("\n6. GRADE PROGRESSION")
print("Average G1:", round(df["G1"].mean(), 2))
print("Average G2:", round(df["G2"].mean(), 2))
print("Average G3:", round(df["G3"].mean(), 2))

# 7. Correlation with final grade
print("\n7. CORRELATION WITH FINAL GRADE")

# 7. CORRELATION WITH FINAL GRADE
print("\n7. CORRELATION WITH FINAL GRADE")

correlation = df[
    ["G1", "G2", "studytime", "absences", "G3"]
].corr()["G3"].drop("G3")

print(correlation.round(3))
print(correlation.round(3))

# 8. Students scoring 10 or below
print("\n8. STUDENTS SCORING 10 OR BELOW")
low_scores = df[df["G3"] <= 10]

print("Student count:", len(low_scores))
print("Percentage:", round(len(low_scores) / len(df) * 100, 2), "%")

print("\nAnalysis completed successfully!")
