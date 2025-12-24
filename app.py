import streamlit as st
import pandas as pd
import plotly.express as px
from logic_engine import HRLogicEngine

# Page Config
st.set_page_config(page_title="LogicHR - 인사 데이터 분석", page_icon="📊", layout="wide")

# Title & Description
st.title("📊 LogicHR: 부서별 성과 및 효율비교")
st.markdown("""
비즈니스 성장을 위한 **데이터 기반 의사결정 도구**입니다.  
부서별 인건비 투입(Input) 대비 성과(Output)를 SQL 엔진으로 분석하여 시각화합니다.
""")

st.markdown("---")

# Sidebar: File Upload
st.sidebar.header("📂 데이터 업로드")
st.sidebar.info("분석할 HR 데이터(CSV, Excel)를 업로드하세요.")

# Helper function to load data
def load_file(uploaded_file):
    if uploaded_file is None:
        return None
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    return None

uploaded_emp = st.sidebar.file_uploader("직원 정보 (Employees)", type=['csv', 'xlsx'])
uploaded_att = st.sidebar.file_uploader("근태 기록 (Attendance)", type=['csv', 'xlsx'])
uploaded_perf = st.sidebar.file_uploader("성과 지표 (Performance)", type=['csv', 'xlsx'])

# Demo Data Toggle
use_demo = st.sidebar.checkbox("데모 데이터 사용해보기", value=True)

df_emp, df_att, df_perf = None, None, None

try:
    if use_demo:
        try:
            df_emp = pd.read_csv('data/employees.csv')
            df_att = pd.read_csv('data/attendance.csv')
            df_perf = pd.read_csv('data/performance.csv')
            st.sidebar.success("✅ 데모 데이터가 로드되었습니다.")
        except FileNotFoundError:
            st.sidebar.error("❌ 데모 데이터를 찾을 수 없습니다. 데이터 생성 스크립트를 실행해주세요.")
    elif uploaded_emp and uploaded_att and uploaded_perf:
        df_emp = load_file(uploaded_emp)
        df_att = load_file(uploaded_att)
        df_perf = load_file(uploaded_perf)
        st.sidebar.success("✅ 파일 업로드 완료!")
    else:
        st.info("👈 왼쪽 사이드바에서 파일을 업로드하거나 '데모 데이터 사용'을 체크해주세요.")
        st.stop()
        
    # Check for required columns (Basic Validation)
    required_cols = {
        'employees': ['emp_id', 'department', 'hourly_rate', 'name'],
        'attendance': ['emp_id', 'check_in', 'check_out', 'date'],
        'performance': ['department', 'target_achievement_rate']
    }
    
    # Simple validation function
    def validate_columns(df, name, required):
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"'{name}' 데이터에 다음 컬럼이 누락되었습니다: {missing}")

    validate_columns(df_emp, "직원 정보", required_cols['employees'])
    validate_columns(df_att, "근태 기록", required_cols['attendance'])
    validate_columns(df_perf, "성과 지표", required_cols['performance'])

    # Initialize Engine
    engine = HRLogicEngine()
    engine.load_data(df_emp, df_att, df_perf)
    
    # Run Analysis
    import time
    start_time = time.time()
    df_dept_analysis = engine.run_department_analysis()
    df_employee_ranking = engine.get_employee_ranking()
    end_time = time.time()
    
    # Sidebar: Engine Status
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Engine Status")
    st.sidebar.success(f"✅ SQLite Engine Active")
    st.sidebar.info(f"⏱️ Query Time: {end_time - start_time:.4f} sec")
    st.sidebar.info(f"📊 Rows Processed: {len(df_att):,}")

    # --- KPI Section ---
    total_cost = df_dept_analysis['total_labor_cost'].sum()
    avg_perf = df_dept_analysis['target_achievement_rate'].mean()
    total_hours = df_dept_analysis['total_hours'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 총 인건비 지출", f"₩{total_cost:,.0f}")
    c2.metric("⏱️ 총 근무 시간", f"{total_hours:,.0f} 시간")
    c3.metric("📈 평균 성과 달성률", f"{avg_perf*100:.1f}%")
    
    # SQL Code Reveal (Moved to Top for Visibility)
    with st.expander("🛠️ [핵심] 이 데이터를 추출한 SQL 로직 보기 (Click to Expand)", expanded=False):
        st.markdown("이 결과는 파이썬이 아닌 **순수 SQL 쿼리**를 통해 계산되었습니다.")
        st.code(engine.get_analysis_query(), language='sql')
    
    st.markdown("---")
    
    # --- Department Analysis Section ---
    st.header("🏆 부서별 효율성 분석 (Efficiency Ranking)")
    
    # Best Department Highlight
    best_dept = df_dept_analysis.iloc[0]
    st.success(f"**🥇 가장 효율적인 부서:** {best_dept['department']} (효율 지수: {best_dept['efficiency_index']})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 효율 지수 (Efficiency Index)")
        st.caption("공식: 부서 성과 / (인건비 / 100만) → 비용 대비 성과가 높을수록 1등")
        fig_eff = px.bar(
            df_dept_analysis,
            x='efficiency_index',
            y='department',
            orientation='h',
            color='efficiency_index',
            title="부서별 효율성 랭킹",
            labels={'efficiency_index': '효율 지수 (Higher is Better)', 'department': '부서'},
            template="plotly_white"
        )
        st.plotly_chart(fig_eff, use_container_width=True)

    with col2:
        st.markdown("#### 비용 vs 성과 매트릭스")
        fig_scatter = px.scatter(
            df_dept_analysis,
            x='total_labor_cost',
            y='target_achievement_rate',
            size='active_headcount',
            color='department',
            hover_name='department',
            title="ROI Matrix",
            labels={
                'total_labor_cost': '총 투입 인건비 (Input)',
                'target_achievement_rate': '목표 달성률 (Output)'
            },
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # --- Detail Tabs ---
    tab1, tab2 = st.tabs(["📊 상세 차트", "📋 데이터 테이블"])
    
    with tab1:
        c_a, c_b = st.columns(2)
        with c_a: # ... column content remains same as previous but needs careful replacement if I replace the whole block
            fig_cost = px.pie(df_dept_analysis, values='total_labor_cost', names='department', title="인건비 구성 비율")
            st.plotly_chart(fig_cost, use_container_width=True)
        with c_b:
            fig_perf = px.bar(df_dept_analysis, x='department', y='target_achievement_rate', title="부서별 목표 달성률")
            st.plotly_chart(fig_perf, use_container_width=True)
            
    with tab2:
        st.subheader("직원별 근태 랭킹 Top 10")
        display_ranking = df_employee_ranking.rename(columns={
            'name': '이름',
            'department': '부서',
            'level': '직급',
            'total_hours': '총 근무시간'
        })
        st.table(display_ranking)

        st.subheader("부서별 통합 지표")
        st.dataframe(df_dept_analysis)
        


except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
