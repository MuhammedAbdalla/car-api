import logging
import os

class Color:
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def setup_logging():
    log_file_path = os.path.join(os.path.dirname(__file__), 'logs/app.log')
    
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'logs')):
        os.mkdir('logs')
    
    logging.basicConfig(
        filename=log_file_path, 
        level=logging.INFO, 
        filemode='a', 
        format='%(asctime)s [%(process)d %(name)s] %(levelname)s: %(message)s'
    )

def send_sys_msg(text):
    logging.info(text)

def send_sys_log(text, funcName):
    logging.debug(f'<{funcName}> : {text}')

def send_sys_err(text, funcName, level):
    if level == logging.WARN:
        logging.warning(f'{Color.YELLOW}    <{funcName}> : {text}  {Color.RESET}')
    if level == logging.ERROR:
        logging.error(f'{Color.ORANGE}      <{funcName}> : {text}  {Color.RESET}')
    if level == logging.CRITICAL:
        logging.critical(f'{Color.RED}      <{funcName}> : {text}  {Color.RESET}')



# implement query for logs
# implement change for log file, and format