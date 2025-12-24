# Product Requirements Document (PRD) - LogicHR

## 1. 프로젝트 개요 (Project Overview)
- **프로젝트명**: LogicHR (부서별 투입 공수 대비 성과 분석 솔루션)
- **목표**:
    - 자바(Java) 중심의 개발 능력보다는 **데이터 기반의 비즈니스 문제 정의 및 해결 능력**을 증명.
    - SQL을 활용한 복잡한 데이터 처리 및 논리적 사고력 강조.
    - 현업에서 즉시 활용 가능한 **가벼운 의사결정 지원 도구(MVP)** 구현.

## 2. 해결하고자 하는 문제 (Problem Statement)
- 기업의 인사 담당자는 부서별 인건비 투입 대비 성과 효율을 정확히 파악하기 어려움.
- 기존 HR 툴은 복잡하고 무거우며, 데이터 분석보다는 단순 관리에 초점이 맞춰져 있음.
- **"어느 부서가 가장 효율적으로 일하고 있는가?"**에 대한 정량적 근거 부족.

## 3. 핵심 기능 (MVP Features)
MVP는 화려한 디자인보다 **"데이터 입력 -> SQL 논리 연산 -> 결과 시각화"**의 핵심 파이프라인에 집중한다.

### 3.1. 데이터 입력 (Input)
- **파일 업로드**: 사용자가 엑셀(.xlsx) 또는 CSV 형식의 HR 데이터를 업로드.
- **데이터 포맷**:
    - 필수 포함 항목: 직원 ID, 부서, 직급, 근무시간(출/퇴근), 시급(또는 연봉), 부서별 성과 지표(목표 달성률 등).
- **유효성 검사**: 파일 업로드 시 필수 컬럼 존재 여부 확인.

### 3.2. SQL 로직 엔진 (Processing)
- **임시 DB 구축**: 업로드된 데이터를 메모리 기반 또는 파일 기반 SQLite 데이터베이스에 적재.
- **핵심 연산 (SQL Query)**:
    - **인건비 산출**: `직급별 시급 * 실제 근무시간` (야근/휴일 수당 로직 포함 가능성 고려).
    - **성과 효율 지수(ROI) 계산**: `(부서별 총 성과 / 부서별 총 인건비) * 100`.
    - **부서별 비교**: 부서 그룹핑(`GROUP BY`)을 통한 통계 집계.

### 3.3. 분석 대시보드 (Output)
- **요약 지표**: 전체 인원 수, 총 인건비, 평균 효율 지수 등 KPI 카드 표시.
- **시각화**:
    - 부서별 인건비 비교 (Bar Chart)
    - 부서별 효율성 비교 (Bar/Line Chart)
    - 인건비 구성 비율 (Pie Chart)
- **리포트 뷰**: SQL 연산 결과를 테이블 형태로 제공 및 다운로드 기능 필요 시 고려.

## 4. 기술 스택 (Tech Stack)
- **Language**: Python 3.x
- **Web DB**: SQLite (Python 내장, 별도 서버 구축 불필요)
- **Frontend/UI**: Streamlit (빠른 데이터 앱 프로토타이핑)
- **Development Tool**: Cursor / ChatGPT (Vibe Coding 방법론 적용)

## 5. 데이터 구조 (Preliminary Schema)
*(개발 단계에서 구체화 예정)*
- `employees` (직원 정보: id, name, department, level, hourly_rate)
- `attendance` (근태 정보: emp_id, date, check_in, check_out)
- `performance` (성과 정보: department, target_achievement_rate)

## 6. 개발 및 실행 계획 (Action Plan)
- **1일차**: 데이터 설계 및 가상 데이터 생성 (Mock Data Generation).
- **2~3일차**: SQL 쿼리 로직 설계 및 검증 (핵심 로직 구현).
- **4~5일차**: Streamlit UI 개발 (파일 업로드, 차트 연동).
- **6일차**: 예외 처리 (결측치 처리, 비즈니스 로직 예외 등).
- **7일차**: 문서화 및 포트폴리오 정리 (PRD, 결과 리포트).

## 7. 차별화 포인트 (Selling Point)
- **Logic over Framework**: 복잡한 자바 프레임워크 대신 파이썬/SQL로 비즈니스 로직의 깊이를 보여줌.
- **Real-world Problem Solving**: 단순 CRUD가 아닌, '비용 대비 효율'이라는 실제 기업의 고민을 데이터로 해결.
- **Decision Support**: 인사 담당자가 데이터에 기반한 의사결정을 내릴 수 있도록 돕는 솔루션 지향.
