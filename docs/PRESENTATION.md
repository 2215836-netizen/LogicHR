---
marp: true
theme: gaia
class: lead
paginate: true
backgroundColor: #f0f4f8
style: |
  section {
    font-family: 'Pretendard', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    justify-content: center;
    font-size: 28px;
    padding: 50px;
    background-color: #ffffff;
    color: #2d3748;
    background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  }
  h1 {
    color: #1a365d;
    font-size: 56px;
    font-weight: 800;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  }
  h2 {
    color: #2b6cb0;
    font-size: 40px;
    font-weight: 700;
    border-bottom: 3px solid #4299e1;
    display: inline-block;
    padding-bottom: 10px;
    margin-bottom: 30px;
  }
  h3 {
    font-size: 32px;
    color: #2c5282;
    margin-top: 20px;
  }
  strong {
    color: #e53e3e;
    font-weight: 800;
    background: linear-gradient(120deg, transparent 60%, #fed7d7 60%);
  }
  blockquote {
    background: #ebf8ff;
    border-left: 10px solid #4299e1;
    margin: 20px 0;
    padding: 20px 30px;
    font-style: italic;
    color: #2a4365;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  }
  code {
    background-color: #edf2f7;
    color: #c05621;
    font-family: 'Consolas', 'Monaco', monospace;
    padding: 4px 8px;
    border-radius: 6px;
  }
  li {
    margin-bottom: 12px;
  }
---

# LogicHR
## 데이터로 증명하는 인사이트

> "감(Gut Feeling)이 아닌, **SQL 로직**으로 인사의 효율성을 증명하다"

Team. 2215836-netizen

---

# 1. 문제 정의 (Problem)
### "누가 일을 잘하는가?"

*   **현황**: 많은 기업이 단순히 '매출'이 높거나 '야근'이 많은 부서를 고성과로 착각함
*   **Pain Point**:
    1.  인건비(Input) 대비 성과(Output)를 정량적으로 비교하기 어려움
    2.  특정 부서에서 불필요한 연장 근무(**Leakage**)가 발생해도 감지 못함

---

# 2. 솔루션 (Solution)
### LogicHR: 데이터 기반 HR 의사결정 시스템

*   **Core Engine**: Python + SQLite (In-Memory DB)
*   **Key Metric**: 
    *   효율 지수 (Efficiency Index)
    *   인건비 누수 탐지 (Leakage Detector)
*   **Value**: 복잡한 데이터 속에서 **"비용 효율성"**과 **"리스크"**를 1초 만에 추출

---

# 핵심 기능 1: 효율 지수
### (Efficiency Index)

> "단순한 성과 1등이 아니라, **가성비 1등**을 찾습니다."

*   **Logic**: `(목표 달성률 * 100) / (총 인건비 / 100만)`
*   **SQL 활용**: `JOIN`으로 성과+근태 결합, `Aggregation`으로 비용 집계
*   **효과**: 적은 인원으로 높은 성과를 낸 '숨은 영웅' 부서 발굴

---

# 핵심 기능 2: 인건비 누수 탐지
### (Leakage Detector)

> "데이터 패턴으로 **돈이 새는 구멍**을 막습니다."

*   **Logic**: `GROUP BY day_of_week` & `HAVING avg_hours > 9`
*   **인사이트**: "특정 요일에만 야근이 폭증하지만 성과는 낮은 부서" 경고(Alert)
*   **가치**: 불필요한 초과 근무 수당 절감 및 업무 프로세스 개선

---

# 4. 기술 아키텍처 (Tech Stack)

*   **Language**: Python 3.9+
*   **Database**: **SQLite** 
    *   외부 DB 서버 없이 로컬 파일/메모리에서 고성능 처리
*   **Visualization**: Streamlit, Plotly Express
    *   Interactive Dashboard 구현
*   **Collaboration**: Git, GitHub

---

# 5. 결론 및 기대 효과

1.  **비용 절감**: 비효율적인 연장 근무 패턴 식별 및 개선
2.  **공정한 평가**: 투입 비용까지 고려한 입체적인 성과 평가 가능
3.  **데이터 리터러시**: 직관적인 대시보드와 SQL 공개로 조직 역량 강화

> **"LogicHR은 단순한 대시보드가 아닙니다.**
> **조직의 건강한 성장을 돕는 나침반입니다."**
