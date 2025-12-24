# LogicHR: 데이터 기반 HR 의사결정 솔루션 📊

> **"자바는 툴일 뿐입니다. 중요한 건 비즈니스 로직을 설계하고 데이터를 통해 문제를 해결하는 능력입니다."**

LogicHR은 인사 데이터(근태, 성과, 급여)를 분석하여 **부서별 투입 비용 대비 효율성(ROI)**을 시각화하는 데이터 분석 솔루션입니다.
화려한 프레임워크 대신, **Python과 SQL 엔진**을 직접 설계하여 대용량 데이터를 논리적으로 처리하는 데 집중했습니다.

## 🚀 현업의 문제 해결 (Problem Solving)
기업의 인사 담당자는 "어느 부서가 인건비 대비 가장 높은 성과를 내고 있는가?"라는 질문에 답하기 어렵습니다.
LogicHR은 이를 해결하기 위해 다음과 같은 기능을 제공합니다:

1.  **SQL 로직 엔진 탑재**: 단순 엑셀 수식이 아닌, `SQLite` 기반의 쿼리 엔진이 대규모 데이터를 처리합니다.
2.  **정량적 효율 지수(ROI)**: `(성과 달성률 / 투입 인건비)` 공식을 적용해 모호한 성과를 숫자로 증명합니다.
3.  **즉시 실행 가능한 MVP**: 복잡한 설치 없이 엑셀 파일만 업로드하면 1초 만에 분석 리포트가 생성됩니다.

## 🛠 기술 스택 (Tech Stack)
-   **Core Logic**: Python 3.x, SQLite (In-Memory DB)
-   **SQL Engine**: 복잡한 급여 계산 및 집계 쿼리 직접 구현
-   **Visualization**: Streamlit, Plotly (Interactive Charts)
-   **Collaboration**: Git, GitHub

## 💡 핵심 기능 (Key Features)
### 1. 효율성 랭킹 (Efficiency Ranking)
단순히 매출이 높은 부서가 아니라, **"누가 가장 가성비 좋게 일했는가"**를 보여줍니다.
-   **Input**: 직급별 시급 × 실 근무시간 (야근 포함)
-   **Output**: 부서별 목표 달성률
-   **Logic**: `SQL Window Function` 및 `Aggregation` 활용

### 2. SQL 코드 리빌 (Code Reveal)
개발자의 논리적 사고 과정을 보여주기 위해, 분석에 사용된 **SQL 쿼리 원본을 대시보드에서 직접 공개**합니다.
-   어떻게 데이터를 조인(JOIN)했는지
-   어떻게 결측치를 처리하고 그룹핑(GROUP BY)했는지 확인 가능

### 3. 유연한 데이터 연동
-   CSV 및 Excel(.xlsx) 파일 업로드 지원
-   데이터가 없을 경우를 대비한 **Mock Data Generator** 내장

## 📂 프로젝트 구조
```bash
LogicHR/
├── app.py                # Streamlit 웹 애플리케이션 메인
├── logic_engine.py       # 핵심 비즈니스 로직 (SQL 처리 엔진)
├── scripts/
│   └── data_generator.py # 테스트용 가상 데이터 생성기
├── data/                 # 업로드 테스트용 샘플 데이터
└── docs/
    └── PRD.md            # 기획 및 요구사항 정의서
```

## 💻 실행 방법 (How to Run)
```bash
# 1. 라이브러리 설치
pip install -r requirements.txt

# 2. (옵션) 가상 데이터 생성
python scripts/data_generator.py

# 3. 앱 실행
streamlit run app.py
```

## 👩‍💻 개발자 코멘트
이 프로젝트는 단순한 구현 능력을 넘어, **"데이터를 통해 비즈니스 가치를 창출하는 과정"**을 증명하기 위해 기획되었습니다.
백엔드 로직의 핵심인 `logic_engine.py`에서 제가 어떻게 데이터를 구조화하고 쿼리를 설계했는지 확인해 주세요.
