import sys
import logging
import time
from datetime import datetime
import datetime as dt
import traceback
import json

## Logger 설정    
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
    
    
    
## Main 시작
if __name__ == "__main__":
    
    prj_id = None
    prj_key = 'PJ226584'
    mode = 'INSERT'
    
    
    now = datetime.now()
    start_time = now.strftime('%Y-%m-%d %H:%M:%S')
    now_str_date = now.strftime('%Y-%m-%d')
    now_str_time = now.strftime('%Y-%m-%d %H:%M:%S')
    setup_logger(prj_key, now); 
    logging.debug("=================================================================================================================================")
    logging.debug("Logging START - Program Run Time : " + now_str_time + " / Project Code : " + prj_key)
    logging.debug("=================================================================================================================================")
    
    
    
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
    
    
    # ZOEY : schedule_config
    # schedule_path = str(Path(__file__).parent.absolute()) + '/schedule_config.json'
    try:
        logging.debug("[exportMain.py] check schedule_path config - start")
        # with open(schedule_path) as conf:
        #     logging.debug("Get schedule config")
        #     schedule_config = json.load(conf)
        #     insert_schedule = schedule_config.get("InsertBatch")
        #     logging.debug(insert_schedule)

        #     if now.hour in insert_schedule['schedule']['hour'] : # insert_schedule 시간에 수행되는 배치의 경우 증분 배치가 아니라 전체를 삭제하고 INSERT 한다.
        #         logging.debug("NOW {} Hour!".format(now.hour))
        #         mode = "INSERT"
            
        #     dev_delay_mailing_schedule = schedule_config.get("DevDelayMailing") # 개발자 개발 지연 메일링 여부 설정시간 확인
        #     if now.hour == dev_delay_mailing_schedule['schedule']['hour'] and dev_delay_mailing_schedule['mailingYN'] == 'Y' and datetime.today().weekday() < 5 :
        #         dev_delay_mailing = True # 개발자 지연건 메일링 여부 저장 ( 주말에는 제외하는 로직 추가 Weekday ( 월 : 0, 화 : 1, 수 : 2 ... 일 : 6)  )
    except Exception as e:
        logging.debug('!!! check schedule_path config Exception occured {}'.format(str(e)))
        logging.debug('!!!' + traceback.format_exc())
    finally:
        logging.debug("[exportMain.py] check schedule_path config - end")

    
    try:
        logging.debug('[exportMain.py] Main start')
       
        # jirapath = str(Path(__file__).parent.absolute()) + '/../pwire.json' # jira connection /  pwire.json 파일 경로, pwire.json 에는 jira 로그인 정보가 저장됨.
        # logging.debug('!!!jirapath : ' + jirapath)
        
        # with cnsjira.from_json(jirapath) as cjira: # cnsjira 의 __enter__ 호출, 여기서 pwire.json 파일에서 가져온 정보로 get_jira 호출. get_jira 에서는 auth 정보 검증하여
            
        #     dbpath = str(Path(__file__).parent.absolute()) + '/../database.json' # db connection
        #     with dashboardDB.from_json(dbpath) as db:
                
                # len_prj = 0
                # try:
                #     logging.debug('[exportMain.py] Main Logic start')
        #             targetDateTime = '' # UPSERT 의 경우 정상적으로 수행된 마지막 배치의 시작시점을 가져와야 함
        #             if mode == 'UPSERT' :
        #                 targetDateTimeSql = """select start_timestamp
        #                     from nerpdash_batch_list wbl2
        #                     where batch_id = (
        #                         select max(batch_id)
        #                         from nerpdash_batch_list wbl
        #                         where 1=1
        #                         and   wbl.result = 1
        #                         and   wbl.project_code = '{}'
        #                         and   wbl.end_timestamp is not null
        #                         and   coalesce (wbl.intg_test_yn, 'N') = 'N')""".format(prj_key)
        #                 targetDateTime = db.execute_select_dict(targetDateTimeSql)[0]['start_timestamp'].strftime("%Y-%m-%d %H:%M")

        #             batch_id = db.StartBatch(now, prj_key, 'N')
        #             len_prj = prjwbs.main(cjira, db, prj_key, prj_id) # Pjr. 및 WBS Meta 데이터를 DB에 적재
        #             main_start_time = time.perf_counter()
        #             # startExport(db, cjira, prj_id, prj_key, batch_id, mode, targetDateTime) # 데이터 가져오기 메인
                    
        #             # if dev_delay_mailing : # 개발자 개발 지연건 메일링
        #             #     sendDeveloperDelayEmail.main(db, prj_key, prj_id) 

        #             main_elapsed_time = time.perf_counter() - main_start_time
        #             logging.debug(f'----- startExport elapsed time   {main_elapsed_time:0.4}')
                    
        #             db.updateBatch(batch_id, now, dt.datetime.now(), len_prj, cjira.get_calls(), cjira.get_response_size()) # batch 결과 저장

        #         except Exception as e:
        #             logging.debug('!!!!! exportMain Main Logic Exception occured {}'.format(str(e)))
        #             logging.debug('!!!!!' + traceback.format_exc())
        #             if db is not None:
        #                 db.rollback()
        #                 error_string = f'Exception e: {str(e)} \n {traceback.format_exc()}'
        #                 db.insertBatchFailed(now, dt.datetime.now(), len_prj, cjira.get_calls(), cjira.get_response_size(), error_string)
        #             # error_string = f'Exception e: {str(e)} \n {traceback.format_exc()}' # Add start - (FPT) KhoaTDA1 / ITSM002873-21 - Call send mail function if there is exception 
        #             # sendEmail(prj_key, now, error_string) #  End - (FPT) KhoaTDA1
                    
        #         finally:
        #             logging.debug('----- Main Logic finally')
        #         # import wire_delete_inactive_data as delete_table
        #         # delete_table.main(db) # 불필요 데이터 삭제
        
    except Exception as e:
        logging.debug('!!! exportMain __main__ initialization Exception occured {}'.format(str(e)))
        logging.debug('!!!' + traceback.format_exc())
        # error_string = f'Exception e: {str(e)} \n {traceback.format_exc()}'
        # sendEmail(prj_key, now, error_string)

    finally:
        logging.debug('[exportMain.py] Main finally')
        total_end_time = time.perf_counter()
        total_elapsed_time = total_end_time - total_start_time
        logging.debug('')
        logging.debug('----- started at {} , ended at {}'.format(start_time, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        logging.debug('----- job finished... total elapsed time: {} seconds'.format(time.strftime("%H:%M:%S", time.gmtime(total_elapsed_time))))
        
    
    
    
    
    
    
    