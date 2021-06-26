1. For fetching profiling logs for fetchQuestionId script, run below command:
	python -m cProfile -s tottime fetchQuestionId.py
   It will return profilings logs, questionid and response time.
2. For fetching only questionid and response time, run below command:
	python fetchQuestionId.py
3. For fetching github api profiling logs, run below command:
	python gen_profiler.py
   This will run the api and show profilings logs in a console.
4. For hitting the post request for github api, run below command:
	curl -H "Content-Type: application/json" --request POST -d @test.json http://127.0.0.1:5000/repos
  This will return top 3 respository and its stars count as json input