# PEP 8 코딩 규칙
# 
# 1. 들여쓰기: 공백 4개를 사용하여 들여쓰기합니다.
# 2. 줄 길이: 한 줄의 길이는 79자 이하여야 합니다.
# 3. 빈 줄: 함수 정의와 클래스 정의 사이에는 2개의 빈 줄을 사용하고, 
#    함수 내에는 하나의 빈 줄을 사용합니다.
# 4. import 문: import 문은 항상 파일의 맨 위에 위치하며, 
#    개별적인 import문을 사용하거나 import문 하나에서 
#    여러 모듈을 가져올 수 있습니다.
# 5. 공백: 연산자 주변과 쉼표, 콜론, 세미콜론 주위에는 공백을 사용합니다.
# 6. 명명 규칙: 함수명은 소문자로, 필요한 경우 단어는 밑줄로 구분합니다. 
#    클래스명은 각 단어의 첫 글자를 대문자로 쓰고, 카
#    멜 표기법(CamelCase)을 따릅니다.
# 7. 주석: 주석은 코드에 포함되어 있어야 하며, 
#    명확하고 간결하게 작성해야 합니다.
# 8. Docstrings: 모듈, 클래스, 함수에는 문서화 문자열(docstring)을 포함해야 합니다.


# 8번 항목 샘플

## 함수
def add(a, b) -> int:
    """
    두 숫자를 더하는 함수입니다.

    Args:
        a (int): 첫 번째 숫자
        b (int): 두 번째 숫자

    Returns:
        int: 두 숫자의 합
    """
    return a + b

## 클래스
class Car:
    """
    자동차 클래스입니다.

    Attributes:
        brand (str): 자동차 브랜드
        model (str): 자동차 모델
        year (int): 자동차 출시 년도
    """

    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def display_info(self):
        """
        자동차 정보를 출력하는 메서드입니다.
        """
        print(f"브랜드: {self.brand}, 모델: {self.model}, 출시년도: {self.year}")