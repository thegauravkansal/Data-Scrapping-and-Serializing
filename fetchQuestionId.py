#importing libraries
from hashlib import md5
from requests import post
import logging
from datetime import datetime

def fetchQuestionidAndResponseTime():
    '''
    This function will return the question id and response time of the request.
    '''
    try:
        #creating a data variable in json format
        data = {
                "email": "gauravkansal_01@yahoo.in",
                "name": "gaurav kansal",
                "angel_list": "https://angel.co/gaurav-kansal-4"
                }
        
        #storing email id in email_id variable
        email_id = data['email']
        
        #convertinng email_id into md5 hash object
        hash_password = md5(email_id.encode()).hexdigest()
        logger.info("Email id encoded")
        #creating a header json
        headers = {"x-verloop-password": hash_password}
        
        #url to hit
        url = "https://hiring.verloop.io/api/github-challenge/start/"

        #post a request to a specific url with data and header
        response = post(url, data = data, headers = headers)
        
        
        #storing the url response in json foramt response_data varaible
        response_data = response.json()
        logger.info("response data fetched %s",str(response_data))
        #fetching the question_id from response json
        question_id = response_data['response']['question_id']
        
        #returning question_id
        return question_id
    except Exception as e:
        logger.error('Error:',exc_info = True)
        raise

if __name__ == '__main__':
    
    try:
        #logger object  
        logger = logging.getLogger("ML_Hiring_QuestionId")
        logger.setLevel(logging.INFO)
        
        # create a file handler
        handler = logging.FileHandler('../ML_Hiring/logs/ml_hiring_fetch_question_id.log')
        handler.setLevel(logging.INFO)
        
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # add the handler to the logger
        logger.addHandler(handler)
        
        #response start time
        start_time = datetime.now()
        
        #calling the function
        ques_id = fetchQuestionidAndResponseTime()
        
        #response end time
        end_time = datetime.now() - start_time
        
        logger.info("question id: %s",ques_id)
        
        print("Question Id:",ques_id)
        print("Response Time:", end_time)
    except Exception as e:
        logger.error("Error:",exc_info = True)