#importing libraries
from flask import Flask, request, jsonify
import requests
import logging
from bs4 import BeautifulSoup
import re

#logger object  
logger = logging.getLogger("ML_Hiring")
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('../ML_Hiring/logs/ml_hiring_fetch_github_repos.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(handler)

#app instance
app = Flask(__name__)

@app.route('/repos',methods=['GET','POST'])
def repos():
    ''' This Function will return the top 3 repositiories of an organisation in Github by starts.
        Post json format should be {"org": "organisation_id"}
    '''
    
    try:
        
        if request.method == 'POST':
            #storing the json request to a content variable
            content = request.json  
            
            if content is None:
                logger.info("input is empty")
                return jsonify("Json Input is Empty")
            
            if "org" not in content:
                logger.info("org key not present in json"   )
                return jsonify("'org' key not present in json")
            
            organisation_id = content['org']
            
            #dictionery to store results as key and value has name and star key value pair
            repos = {}

            github_url = "https://github.com/"+organisation_id
            
            request_url = requests.get(github_url)
            
            if request_url.status_code != 200:
                logger.info("invalid organisation name:%s",organisation_id)
                return jsonify("Invalid Organisation Id: " + organisation_id)
            
            #fetching the html text of a url
            html = request_url.content
            
            #initialising beautifulsoup object to parse html
            soup = BeautifulSoup(html,'html.parser') 
            
            #fetching class div tag with class f6 text-gray mt-2
            div = soup.find_all('div',{'class':'f6 text-gray mt-2'}) 
            
            if len(div) == 0:
                logger.info("Not able to find any division tags")
                return jsonify("Not able to find any division tags")
            
            #traversing through every division to find the repositiory name adn stars count
            for d in div:
                
                #find result where tags a href contains 'stargazers'
                temp = d.find('a',attrs = {'href': re.compile("\/stargazers")})
                
                #to check if division a href tag contains result.
                if temp is not None:
                    repository_name = temp.get('href').split("/")[-2]
                    
                    #striping new-line and spacepar from the text string and convert stars count format 1,234 to 1234
                    stars = temp.text.strip("\n ").replace(",","")
                    
                    repos[repository_name] = int(stars)
                    
            #clearing varible memory
            del repository_name, stars 
            
            #sort a dictionery into descending and slicing top 3 count
            if len(repos) == 0:
                return jsonify("Organization does not have any repository")
            elif len(repos) >=3:
                result = sorted(repos.items(),key=lambda x:x[1],reverse=True)[:3]
            else:
                result = sorted(repos.items(),key=lambda x:x[1],reverse=True)
                
            #converting the result into json format
            json_result = []
            for i in result:
                temp = {}
                temp["name"] = i[0]
                temp["stars"] = i[1]
                json_result.append(temp)
            
            logger.info(str(result))
            return jsonify({"results":json_result})

    except Exception:
        logger.error("json decoder error")
        return jsonify("JSON not present")

if __name__ == '__main__':
   app.run(threaded=True,debug=True)