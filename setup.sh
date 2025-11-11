#!/bin/bash

# KREAM 자동 입찰 프로그램 설치 스크립트

echo "╔════════════════════════════════════════════╗"
echo "║   KREAM 자동 입찰 프로그램 설치           ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo "🔧 가상환경 생성 중..."
    python3 -m venv venv
    echo "✅ 가상환경 생성 완료"
else
    echo "✅ 가상환경이 이미 존재합니다"
fi

# 가상환경 활성화
echo ""
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# pip 업그레이드
echo ""
echo "🔧 pip 업그레이드 중..."
pip install --upgrade pip

# 패키지 설치
echo ""
echo "🔧 필요한 패키지 설치 중..."
pip install -r requirements.txt

# 디렉토리 생성
echo ""
echo "🔧 필요한 디렉토리 생성 중..."
mkdir -p logs data screenshots

# .env 파일 확인
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다"
    echo "📝 .env.example을 복사하여 .env 파일을 생성하고 설정해주세요"
    cp .env.example .env
    echo "✅ .env 파일이 생성되었습니다. 편집해주세요!"
else
    echo "✅ .env 파일이 이미 존재합니다"
fi

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   설치 완료!                              ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "다음 명령어로 프로그램을 실행하세요:"
echo ""
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""

