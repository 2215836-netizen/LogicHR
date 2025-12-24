import sqlite3
import pandas as pd
import numpy as np

class HRLogicEngine:
    def __init__(self):
        # Create an in-memory SQLite database
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def load_data(self, df_employees, df_attendance, df_performance):
        """
        Load Pandas DataFrames into SQLite tables.
        """
        df_employees.to_sql('employees', self.conn, index=False, if_exists='replace')
        df_attendance.to_sql('attendance', self.conn, index=False, if_exists='replace')
        df_performance.to_sql('performance', self.conn, index=False, if_exists='replace')

    def run_cost_calculation(self):
        """
        Calculate daily work hours and cost for each attendance record.
        SQL logic:
        1. Parse check_in and check_out to calculate hours worked.
        2. Join with employees to get hourly_rate.
        3. Cost = Hours * Rate.
        """
        query = """
        SELECT 
            a.emp_id,
            e.name,
            e.department,
            e.level,
            a.date,
            a.check_in,
            a.check_out,
            e.hourly_rate,
            -- Calculate Hours Worked (handling potential NULLs or cross-day is simplified here)
            (julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24 AS hours_worked,
            
            -- Calculate Cost
            ((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) * e.hourly_rate AS daily_cost
        FROM attendance a
        JOIN employees e ON a.emp_id = e.emp_id
        WHERE a.check_out IS NOT NULL AND a.check_in IS NOT NULL
        """
        return pd.read_sql_query(query, self.conn)

    def run_department_analysis(self):
        """
        Aggregate costs by department and compare with performance.
        Includes specific 'Efficiency Index' Calculation.
        """
        query = """
        WITH DeptStats AS (
            SELECT 
                e.department,
                COUNT(DISTINCT a.emp_id) as active_headcount,
                SUM((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) as total_hours,
                SUM(((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) * e.hourly_rate) as total_labor_cost
            FROM attendance a
            JOIN employees e ON a.emp_id = e.emp_id
            WHERE a.check_out IS NOT NULL
            GROUP BY e.department
        )
        SELECT 
            d.department,
            d.active_headcount,
            CAST(d.total_hours AS INTEGER) as total_hours,
            CAST(d.total_labor_cost AS INTEGER) as total_labor_cost,
            p.target_achievement_rate,
            
            -- Efficiency Index (ROI) Calculation
            -- Logic: (Performance Score / Cost in Millions) * 10
            -- Higher is better. A department with high performance and low cost gets a high score.
            ROUND((p.target_achievement_rate * 100) / (d.total_labor_cost / 1000000.0), 2) as efficiency_index
        FROM DeptStats d
        JOIN performance p ON d.department = p.department
        ORDER BY efficiency_index DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_analysis_query(self):
        """Returns the SQL query used for department analysis for display purposes."""
        return """
        WITH DeptStats AS (
            SELECT 
                e.department,
                COUNT(DISTINCT a.emp_id) as active_headcount,
                SUM((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) as total_hours,
                SUM(((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) * e.hourly_rate) as total_labor_cost
            FROM attendance a
            JOIN employees e ON a.emp_id = e.emp_id
            WHERE a.check_out IS NOT NULL
            GROUP BY e.department
        )
        SELECT 
            d.department,
            d.active_headcount,
            d.total_hours,
            d.total_labor_cost,
            p.target_achievement_rate,
            
            -- 효율 지수 (ROI) 계산 로직
            -- (목표 달성률 * 100) / (총 인건비 / 100만)
            ROUND((p.target_achievement_rate * 100) / (d.total_labor_cost / 1000000.0), 2) as efficiency_index
        FROM DeptStats d
        JOIN performance p ON d.department = p.department
        ORDER BY efficiency_index DESC
        """
    def get_employee_ranking(self):
        """
        Rank employees by total hours worked (Hardest workers?)
        """
        query = """
        SELECT 
            e.name,
            e.department,
            e.level,
            SUM((julianday(a.date || ' ' || a.check_out) - julianday(a.date || ' ' || a.check_in)) * 24) as total_hours
        FROM attendance a
        JOIN employees e ON a.emp_id = e.emp_id
        WHERE a.check_out IS NOT NULL
        GROUP BY e.emp_id
        ORDER BY total_hours DESC
        LIMIT 10
        """
        return pd.read_sql_query(query, self.conn)
