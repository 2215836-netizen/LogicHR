import pandas as pd
from logic_engine import HRLogicEngine

# Load Mock Data
print("Loading data...")
df_emp = pd.read_csv('data/employees.csv')
df_att = pd.read_csv('data/attendance.csv')
df_perf = pd.read_csv('data/performance.csv')

# Initialize Engine
engine = HRLogicEngine()
engine.load_data(df_emp, df_att, df_perf)

# 1. Test Cost Calculation
print("\n--- [Test 1] individual Cost Calculation (Top 5) ---")
df_cost = engine.run_cost_calculation()
print(df_cost[['date', 'name', 'department', 'hours_worked', 'daily_cost']].head())

# 2. Test Department Analysis
print("\n--- [Test 2] Department Analysis ---")
df_dept = engine.run_department_analysis()
print(df_dept)

# 3. Test Employee Ranking
print("\n--- [Test 3] Top 5 Hardest Workers ---")
df_rank = engine.get_employee_ranking()
print(df_rank.head())

print("\nSQL Logic Verification Complete.")
