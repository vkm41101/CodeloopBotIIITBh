import requests
apiUrl = 'https://codeforces.com/api'
def dumpProblemSet():
    url = apiUrl + '/problemset.problems'
    problems = requests.get(url)
    with open('problemset.json', 'w+', encoding='utf-8') as file:
        file.write(problems.text)
    return None
dumpProblemSet()
