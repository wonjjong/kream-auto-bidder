# KREAM 자동 입찰 프로그램 사용 가이드

## 📋 목차

1. [빠른 시작](#빠른-시작)
2. [설정 방법](#설정-방법)
3. [사용법](#사용법)
4. [고급 설정](#고급-설정)
5. [문제 해결](#문제-해결)

---

## 🚀 빠른 시작

### 1. 설치

```bash
# 1. 프로젝트 디렉토리로 이동
cd kream-auto-bidder

# 2. 설치 스크립트 실행
./setup.sh

# 3. 가상환경 활성화
source venv/bin/activate

# 4. 설치 테스트
python test_setup.py
```

### 2. 환경 설정

```bash
# .env 파일 편집 (계정 정보 입력)
nano .env
```

`.env` 파일 예시:
```
KREAM_EMAIL=your_email@example.com
KREAM_PASSWORD=your_password
TARGET_PRICE=100000
MAX_PRICE=150000
```

### 3. 실행

```bash
# 메인 프로그램 실행
python main.py

# 또는 실행 스크립트 사용
./run.sh
```

---

## ⚙️ 설정 방법

### config.yaml 설정

```yaml
browser:
  headless: false          # true: 브라우저 창 숨김
  implicit_wait: 10        # 요소 대기 시간
  page_load_timeout: 30    # 페이지 로드 타임아웃

crawler:
  check_interval: 60       # 가격 확인 주기 (초)
  request_delay: 2         # 요청 간 대기 시간
  max_retries: 3          # 최대 재시도 횟수

bidding:
  auto_bid: true          # 자동 입찰 활성화
  min_price: 50000        # 최소 입찰 가격
  max_price: 200000       # 최대 입찰 가격
  target_price: 100000    # 목표 입찰 가격
  price_step: 1000        # 가격 단위
```

---

## 📖 사용법

### 1. 가격 모니터링만 하기

특정 상품의 가격 변동을 모니터링합니다.

```bash
python price_monitor.py \
  --product-url "https://kream.co.kr/products/12345" \
  --size 270 \
  --duration 3600
```

**옵션:**
- `--product-url`: 상품 URL (필수)
- `--size`: 사이즈 (선택)
- `--duration`: 모니터링 시간(초) (선택, 미지정시 무한)

### 2. 자동 입찰 실행

가격을 모니터링하고 조건에 맞으면 자동으로 입찰합니다.

```bash
python auto_bidder.py \
  --product-url "https://kream.co.kr/products/12345" \
  --size 270 \
  --target-price 100000 \
  --max-price 150000
```

**옵션:**
- `--product-url`: 상품 URL (필수)
- `--size`: 사이즈 (필수)
- `--target-price`: 목표 가격 (선택)
- `--max-price`: 최대 가격 (선택)

### 3. 대화형 모드로 실행

```bash
python main.py
```

프로그램이 단계별로 정보를 요청합니다:
1. 상품 URL 입력
2. 사이즈 입력
3. 목표 가격 입력
4. 최대 가격 입력
5. 설정 확인 후 실행

---

## 🔧 고급 설정

### 헤드리스 모드 (브라우저 창 숨김)

브라우저 창을 표시하지 않고 백그라운드에서 실행:

```python
# kream_crawler.py 수정
crawler = KreamCrawler(headless=True)
```

또는 `config.yaml`에서:
```yaml
browser:
  headless: true
```

### 로깅 레벨 변경

더 자세한 로그를 보고 싶다면:

```python
# utils.py의 setup_logger 함수 호출시
logger = setup_logger('name', 'logs/app.log', level=logging.DEBUG)
```

### 요청 간격 조정

서버 부하를 줄이기 위해 요청 간격을 늘리세요:

```yaml
crawler:
  check_interval: 120  # 2분마다 확인
  request_delay: 5     # 요청 간 5초 대기
```

---

## 🐛 문제 해결

### 1. 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 특정 패키지 재설치
pip install --force-reinstall selenium
```

### 2. ChromeDriver 오류

```bash
# webdriver-manager가 자동으로 처리하지만, 수동 설치 필요시:
pip install --upgrade webdriver-manager
```

### 3. 로그인 실패

- `.env` 파일의 이메일/비밀번호 확인
- KREAM의 2단계 인증 확인
- 수동 로그인 후 30초 대기 시간 활용

### 4. 상품 정보를 가져올 수 없음

KREAM의 웹사이트 구조가 변경되었을 수 있습니다.
`kream_crawler.py`의 셀렉터를 업데이트해야 합니다.

### 5. 자동화 감지

일부 웹사이트는 Selenium 자동화를 감지합니다:
- `headless: false`로 설정
- User-Agent 변경
- 요청 간격 늘리기

---

## 📊 데이터 저장 위치

- **로그 파일**: `logs/` 디렉토리
  - `crawler.log`: 크롤러 로그
  - `price_monitor.log`: 가격 모니터링 로그
  - `auto_bidder.log`: 자동 입찰 로그
  - `main.log`: 메인 프로그램 로그

- **수집 데이터**: `data/` 디렉토리
  - `price_history_*.csv`: 가격 이력 데이터

- **스크린샷**: `screenshots/` 디렉토리

---

## ⚠️ 주의사항

1. **법적 책임**: 본 프로그램 사용으로 인한 모든 책임은 사용자에게 있습니다.

2. **서비스 약관**: KREAM의 이용약관을 반드시 확인하세요.

3. **과도한 요청**: 서버에 부담을 주지 않도록 적절한 간격을 설정하세요.

4. **계정 보안**: `.env` 파일을 Git에 커밋하지 마세요.

5. **테스트 모드**: 실제 입찰 로직은 구현되지 않았습니다. 실사용을 위해서는 KREAM의 실제 HTML 구조에 맞게 코드를 수정해야 합니다.

---

## 📞 도움말

더 자세한 정보는 다음 파일을 참조하세요:
- `README.md`: 프로젝트 개요
- 각 Python 파일의 docstring
- 로그 파일

---

**행복한 코딩 되세요! 🎉**

