# 서비스 리턴 코드
OK = 200                    # GET 서비스 정상 종료

CREATED = 201               # POST 서비스 정상 종료
CR = 201                    # POST 서비스 정상 종료

NO_CONTENT = 204            # 정상적으로 GET 서비스 수행(리턴값 없음)
NC = 204                    # 정상적으로 GET 서비스 수행(리턴값 없음)

BAD_REQUEST = 400           # 요청을 서버가 이해 못함(파라미터 오류)
BR = 400                    # 요청을 서버가 이해 못함(파라미터 오류)

UNAUTHORIZED = 401          # 인증실패
UA = 401                    # 인증실패

FORBIDDEN = 403             # 접근권한 오류
FB = 403                    # 접근권한 오류

NOT_FOUND = 404             # 요청을 서버가 이해 못함(라우팅 오류)
NF = 404                    # 요청을 서버가 이해 못함(라우팅 오류)

METHOD_NOT_ALLOWED = 405    # 요청 메서드 접근권한 오류
MNA = 405                   # 요청 메서드 접근권한 오류

INTERNAL_SERVER_ERROR = 500 # Internal Server Error 서비스 실행중 오류
ISE = 500                   # Internal Server Error 서비스 실행중 오류