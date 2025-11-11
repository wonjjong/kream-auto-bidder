"""
설치 테스트 스크립트
"""
import sys

def test_imports():
    """필요한 패키지 임포트 테스트"""
    print("패키지 임포트 테스트 시작...\n")
    
    packages = [
        ('selenium', 'Selenium'),
        ('webdriver_manager', 'WebDriver Manager'),
        ('requests', 'Requests'),
        ('bs4', 'BeautifulSoup4'),
        ('pandas', 'Pandas'),
        ('dotenv', 'Python-dotenv'),
        ('yaml', 'PyYAML'),
    ]
    
    success = 0
    failed = 0
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name}: 설치됨")
            success += 1
        except ImportError:
            print(f"❌ {name}: 설치되지 않음")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"성공: {success}개, 실패: {failed}개")
    print(f"{'='*50}\n")
    
    if failed > 0:
        print("⚠️  일부 패키지가 설치되지 않았습니다.")
        print("다음 명령어로 패키지를 설치하세요:")
        print("  source venv/bin/activate")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("✅ 모든 패키지가 정상적으로 설치되었습니다!")
        return True


def test_files():
    """필요한 파일 존재 확인"""
    import os
    
    print("\n파일 존재 확인...\n")
    
    required_files = [
        'requirements.txt',
        'config.yaml',
        '.env.example',
        'main.py',
        'kream_crawler.py',
        'auto_bidder.py',
        'price_monitor.py',
        'utils.py',
        'README.md',
    ]
    
    success = 0
    failed = 0
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: 존재함")
            success += 1
        else:
            print(f"❌ {file}: 존재하지 않음")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"성공: {success}개, 실패: {failed}개")
    print(f"{'='*50}\n")
    
    return failed == 0


def test_directories():
    """필요한 디렉토리 존재 확인"""
    import os
    
    print("\n디렉토리 존재 확인...\n")
    
    required_dirs = ['logs', 'data', 'screenshots', 'venv']
    
    success = 0
    failed = 0
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"✅ {directory}/: 존재함")
            success += 1
        else:
            print(f"❌ {directory}/: 존재하지 않음")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"성공: {success}개, 실패: {failed}개")
    print(f"{'='*50}\n")
    
    return failed == 0


def main():
    """메인 테스트 함수"""
    print("\n╔════════════════════════════════════════════╗")
    print("║   KREAM 자동 입찰 프로그램 설치 테스트   ║")
    print("╚════════════════════════════════════════════╝\n")
    
    # 파일 테스트
    files_ok = test_files()
    
    # 디렉토리 테스트
    dirs_ok = test_directories()
    
    # 패키지 임포트 테스트
    imports_ok = test_imports()
    
    # 최종 결과
    print("\n╔════════════════════════════════════════════╗")
    print("║   테스트 결과                             ║")
    print("╚════════════════════════════════════════════╝\n")
    
    if files_ok and dirs_ok and imports_ok:
        print("✅ 모든 테스트 통과!")
        print("\n프로그램을 사용할 준비가 되었습니다.")
        print("\n실행 방법:")
        print("  python main.py")
        return 0
    else:
        print("❌ 일부 테스트 실패")
        print("\nsetup.sh 스크립트를 다시 실행해보세요:")
        print("  ./setup.sh")
        return 1


if __name__ == "__main__":
    sys.exit(main())

