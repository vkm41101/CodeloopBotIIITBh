import requests
import json

apiUrl = 'https://codeforces.com/api'


def getAllProblemsSolved(handle):
    listOfProblems = []
    url = apiUrl + f'/user.status?handle={handle}'
    problems = requests.get(url)
    problems = json.loads(problems.text)
    problems = problems["result"]
    for problem in problems:
        if problem["verdict"] == "OK":
            listOfProblems.append(str(problem['problem']['contestId']) + problem['problem']['index'])
    listOfProblems = list(set(listOfProblems))
    return listOfProblems


def getProblemsOfRating(start: int = 800, stop: int = -1):
    if stop == -1:
        stop = start + 400
    listOfProblems = []
    problemSet=''
    with open('problemset.json', 'r', encoding='utf-8') as file:
        problemSet=file.read()
    problems = json.loads(problemSet)
    problems = problems['result']['problems']
    for problem in problems:
        if 'rating' not in problem:
            continue
        rat=problem['rating']
        if start <= rat <= stop:
            listOfProblems.append(str(problem['contestId']) + problem['index'])
    return listOfProblems

def generateChallenge(challengerUsername: str, challengeeUsername: str, baseRating:int = 800):
    challengerProblemsSolved=getAllProblemsSolved(challengerUsername)
    challengeeProblemsSolved=getAllProblemsSolved(challengeeUsername)
    listOfProblems=[]
    problemSet=getProblemsOfRating(baseRating, baseRating+400)
    for problem in problemSet:
        if len(listOfProblems) == 5:
            break
        if problem not in challengerProblemsSolved and problem not in challengeeProblemsSolved:
            listOfProblems.append(problem)
    return listOfProblems



