import requests

def send_deletion_request(url, email, reason):
     """
    웹사이트에 삭제 요청을 자동으로 보내는 함수입니다.
    
    :param url: 삭제 요청할 웹 페이지 URL
    :param email: 요청자의 이메일 주소
    :param reason: 삭제 요청 사유
    """
     # 삭제 요청을 위한 URL (실제 웹사이트에 맞게 변경해야 합니다)
     deletion_url = "https://example.com/delete_request"
     
     #삭제 요청 데이터
     data = {
         'url' : url,
         'email' : email,
         'reason' : reason
     }
     
     try:
         #POST 요청 보내기
         response = requests.post(deletion.url, data=data)
         
         #응답 상태 코드 확인
         if response.status_code == 200:
             print("삭제 요청이 성공적으로 제출되었습니다.")
         else:
             print(f'삭제 요청 제출 실패: {response.status_code}')
     except Exception as e:
         print(f'오류 발생: {e}')

if __name__ == "__main__":
    #사용자 입력
    url = input("삭제 요청할 URL을 입력하세요: ")
    email = input("이메일 주소를 입력하세요: ")
    reason = input("삭제 요청 사유를 입력하세요: ")
    
    # 삭제 요청 함수 호출
    send_deletion_request(url, email, reason)
               