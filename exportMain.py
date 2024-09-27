import sys
import logging
import time
from datetime import datetime
import datetime as dt
import traceback

    
def setup_logger(prj_key, now = datetime.now()):
    file_name = './log/' + prj_key + '_' + now_str_date + '.log'
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # 로그 출력 포멧
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter) 
    logger.addHandler(stream_handler) # 로그를 콘솔에 출력
    
    file_handler = logging.FileHandler(file_name, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler) # 로그를 파일에 출력
    
    
    
## 메인 시작
if __name__ == "__main__":
    
    prj_id = None
    prj_key = 'PJ226584'
    mode = 'INSERT'
    
    
    now = datetime.now()
    start_time = now.strftime('%Y-%m-%d %H:%M:%S')
    now_str_date = now.strftime('%Y-%m-%d')
    now_str_time = now.strftime('%Y-%m-%d %H:%M:%S')
    setup_logger(prj_key, now); 
    
    
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=False) # 표준출력 / utf-8
    sys.stderr = open(2, 'w', encoding='utf-8', closefd=False) # 표준에러출력 / utf-8
    ### 설명(sys.stdout, sys.stderr 재지정)
    # 1. print(), 에러 등 출력할 내용을 각 파일 객체(stdout,stderr)를 통해 표준출력/표준에러출력으로 전달하는 역할 
    # 2. stdout,stderr를 파일 객체로 재지정하여 출력결과를 리다이렉션하여 파일로 저장할 수 있단 장점이 있음
    # 3. 일반메시지와 오류메시지가 분리되어 출력되어, 일반메시지와 오류메시지를 구분하기에 유용함
    
    
    ## 프로그램 실행 시 입력한 파라미터 받아오기
    args = sys.argv
    if (len(sys.argv) > 1):
        for argument in args:
            preArg = argument[:3]
            if (preArg == "-i="):
                prj_id = argument[3:]
            if (preArg == "-k="):
                prj_key = argument[3:]
            if (preArg == "-m="):
                mode = argument[3:]
    total_start_time = time.perf_counter() # ex.0.0834604 : 프로그램이 시작된 이후의 시간을 초 단위로 반환
    logging.debug("args : " + str(args))
    logging.debug("Project ID : " + str(prj_id) + ", Project Key : " + prj_key + ", Mode : " + mode)
    
    
    #TODO : schedule_config
    
    
    try:
        logging.debug('----- Main Logic start')
    except Exception as e:
        logging.debug('!!! exportMain __main__ initialization Exception occured {}'.format(str(e)))
        logging.debug('!!!' + traceback.format_exc())

        # error_string = f'Exception e: {str(e)} \n {traceback.format_exc()}'
        # sendEmail(prj_key, now, error_string)

    finally:
        total_end_time = time.perf_counter()
        total_elapsed_time = total_end_time - total_start_time
        logging.debug('')
        logging.debug('----- started at {} , ended at {}'.format(start_time, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logging.debug('----- job finished... total elapsed time: {} seconds'.format(time.strftime("%H:%M:%S", time.gmtime(total_elapsed_time))))
        
    
    
    
    
    
    
    