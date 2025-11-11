# KREAM 자동 판매 입찰 프로그램

KREAM 플랫폼의 판매 입찰을 자동화하는 파이썬 프로그램입니다.

## ⚠️ 중요 주의사항

**이 프로그램은 교육 목적으로만 제공됩니다.**

- KREAM 서비스 약관을 반드시 확인하세요
- 자동화 프로그램 사용이 약관 위반일 수 있습니다
- 과도한 요청으로 서버에 부담을 주지 마세요
- 계정 제재나 법적 문제가 발생할 수 있습니다
- 본인 책임하에 사용하세요

## 기능

- 🔍 상품 가격 실시간 모니터링
- 💰 자동 판매 입찰
- 📊 가격 변동 추적 및 저장
- 🔔 입찰 성공/실패 알림
- 📈 통계 및 분석 리포트

## 설치 방법

### 1. 저장소 클론

```bash
cd kream-auto-bidder
```

### 2. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어서 실제 계정 정보 입력
```

### 5. 설정 파일 수정

`config.yaml` 파일에서 입찰 설정을 원하는 대로 수정하세요.

## 사용 방법

### 가격 모니터링

```bash
python price_monitor.py --product-url "https://kream.co.kr/products/xxxxx"
```

### 자동 입찰 실행

```bash
python auto_bidder.py --product-url "https://kream.co.kr/products/xxxxx" --size 270
```

### 전체 프로그램 실행

```bash
python main.py
```

## 프로젝트 구조

```
kream-auto-bidder/
├── venv/                    # 가상환경
├── logs/                    # 로그 파일
├── data/                    # 수집된 데이터
├── config.yaml             # 설정 파일
├── .env                    # 환경 변수 (계정 정보)
├── requirements.txt        # 필요한 패키지
├── main.py                 # 메인 실행 파일
├── kream_crawler.py        # KREAM 크롤러
├── auto_bidder.py          # 자동 입찰 모듈
├── price_monitor.py        # 가격 모니터링
├── utils.py                # 유틸리티 함수
└── README.md               # 프로젝트 설명
```

## 설정 옵션

### config.yaml

- `browser.headless`: 브라우저 창 표시 여부
- `crawler.check_interval`: 가격 확인 주기 (초)
- `bidding.target_price`: 목표 입찰 가격
- `bidding.max_price`: 최대 입찰 가격

## 예시

```python
from auto_bidder import KreamAutoBidder

# 자동 입찰 시작
bidder = KreamAutoBidder()
bidder.login()
bidder.monitor_and_bid(
    product_url="https://kream.co.kr/products/12345",
    size="270",
    target_price=100000
)
```

## 법적 고지

이 소프트웨어는 교육 및 연구 목적으로만 제공됩니다. 사용자는 다음 사항을 준수해야 합니다:

1. 해당 웹사이트의 이용약관 및 robots.txt 준수
2. 과도한 트래픽 생성 금지
3. 개인정보 보호법 준수
4. 저작권 및 관련 법률 준수

본 프로그램 사용으로 인한 모든 책임은 사용자에게 있습니다.

## 라이선스

MIT License

