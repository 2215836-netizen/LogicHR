import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker('ko_KR')  # Korean locale
Faker.seed(42)
random.seed(42)

# Configuration
NUM_EMPLOYEES = 50
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 1, 31)
DEPARTMENTS = ['Sales', 'Engineering', 'HR', 'Marketing', 'Finance']
LEVELS = ['Junior', 'Senior', 'Manager', 'Director']
HOURLY_RATES = {
    'Junior': 15000,
    'Senior': 25000,
    'Manager': 40000,
    'Director': 60000
}

def generate_employees(num):
    employees = []
    for _ in range(num):
        level = random.choice(LEVELS)
        employees.append({
            'emp_id': fake.unique.random_number(digits=6),
            'name': fake.name(),
            'department': random.choice(DEPARTMENTS),
            'level': level,
            'hourly_rate': HOURLY_RATES[level]
        })
    return pd.DataFrame(employees)

def generate_attendance(employees, start_date, end_date):
    attendance_records = []
    
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
            
        for _, emp in employees.iterrows():
            # 5% chance of absence
            if random.random() < 0.05:
                continue
                
            # Random check-in time (08:30 - 09:30)
            check_in_base = current_date.replace(hour=8, minute=30)
            check_in = check_in_base + timedelta(minutes=random.randint(0, 60))
            
            # Random check-out time (17:30 - 19:30), sometimes missing (e.g., 2% chance error)
            if random.random() < 0.02:
                check_out = None # Simulation of missing punch-out
            else:
                check_out_base = current_date.replace(hour=17, minute=30)
                check_out = check_out_base + timedelta(minutes=random.randint(0, 120))
            
            attendance_records.append({
                'emp_id': emp['emp_id'],
                'date': current_date.strftime('%Y-%m-%d'),
                'check_in': check_in.strftime('%H:%M:%S'),
                'check_out': check_out.strftime('%H:%M:%S') if check_out else None
            })
        
        current_date += timedelta(days=1)
        
    return pd.DataFrame(attendance_records)

def generate_performance(departments):
    performance_records = []
    for dept in departments:
        # Random target achievement rate (70% - 130%)
        achievement_rate = round(random.uniform(0.7, 1.3), 2)
        performance_records.append({
            'department': dept,
            'target_achievement_rate': achievement_rate,
            'evaluation_period': '2024-01'
        })
    return pd.DataFrame(performance_records)

def main():
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')
        
    print("Generating employees...")
    df_employees = generate_employees(NUM_EMPLOYEES)
    df_employees.to_csv('data/employees.csv', index=False, encoding='utf-8-sig')
    df_employees.to_excel('data/employees.xlsx', index=False)
    
    print("Generating attendance...")
    df_attendance = generate_attendance(df_employees, START_DATE, END_DATE)
    df_attendance.to_csv('data/attendance.csv', index=False, encoding='utf-8-sig')
    df_attendance.to_excel('data/attendance.xlsx', index=False)
    
    print("Generating performance...")
    df_performance = generate_performance(DEPARTMENTS)
    df_performance.to_csv('data/performance.csv', index=False, encoding='utf-8-sig')
    df_performance.to_excel('data/performance.xlsx', index=False)
    
    print("Data generation complete! Check the 'data' folder for CSV and Excel files.")

if __name__ == "__main__":
    main()
