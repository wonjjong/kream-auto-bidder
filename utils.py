"""
유틸리티 함수 모음
"""
import os
import logging
import pandas as pd
from datetime import datetime
import yaml
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


def setup_logger(name, log_file=None, level=logging.INFO):
    """
    로거 설정
    
    Args:
        name (str): 로거 이름
        log_file (str): 로그 파일 경로
        level: 로그 레벨
        
    Returns:
        logging.Logger: 설정된 로거
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def load_config(config_file='config.yaml'):
    """
    YAML 설정 파일 로드
    
    Args:
        config_file (str): 설정 파일 경로
        
    Returns:
        dict: 설정 딕셔너리
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"설정 파일 로드 실패: {e}")
        return {}


def get_env(key, default=None):
    """
    환경 변수 가져오기
    
    Args:
        key (str): 환경 변수 키
        default: 기본값
        
    Returns:
        환경 변수 값
    """
    return os.getenv(key, default)


def save_to_csv(data, filename):
    """
    데이터를 CSV 파일로 저장
    
    Args:
        data: DataFrame 또는 리스트
        filename (str): 저장할 파일명
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"데이터 저장 완료: {filename}")
    except Exception as e:
        print(f"CSV 저장 실패: {e}")


def save_to_excel(data, filename):
    """
    데이터를 Excel 파일로 저장
    
    Args:
        data: DataFrame 또는 리스트
        filename (str): 저장할 파일명
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
        
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"데이터 저장 완료: {filename}")
    except Exception as e:
        print(f"Excel 저장 실패: {e}")


def format_price(price):
    """
    가격 포맷팅 (원화)
    
    Args:
        price (int): 가격
        
    Returns:
        str: 포맷된 가격 문자열
    """
    return f"{price:,}원"


def parse_price(price_str):
    """
    가격 문자열을 숫자로 변환
    
    Args:
        price_str (str): 가격 문자열 (예: "100,000원")
        
    Returns:
        int: 숫자 가격
    """
    try:
        # 숫자가 아닌 문자 제거
        price = ''.join(filter(str.isdigit, price_str))
        return int(price) if price else 0
    except Exception as e:
        print(f"가격 파싱 실패: {e}")
        return 0


def get_timestamp():
    """
    현재 타임스탬프 반환
    
    Returns:
        str: 포맷된 타임스탬프
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_directories():
    """필요한 디렉토리 생성"""
    directories = ['logs', 'data', 'screenshots']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

