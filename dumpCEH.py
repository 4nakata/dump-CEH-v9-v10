# /usr/bin/python
from bs4 import BeautifulSoup
import requests
import re
import sys

_regexAnswers = '(A\..*\n?.*)\n*(B\..*\n?.*)\n*(C\..*\n?.*)\n*(D\..*\n?.*)\n*|(A\..*)(B\..*)'


def getHTMLCode(_url):
    try:
        _response = requests.get(_url)
        return BeautifulSoup(_response.text, 'html.parser')

    except requests.exceptions.ConnectionError:
        return getHTMLCode(_url)


def initFile(_tmpFile, _numberQuestions, _versionCEH):
    with open(_tmpFile, 'w') as _file:
        _file.write('\n ' + str(_numberQuestions) + ' Questions  - CEH' + _versionCEH + '\n')
    _file.close()


def writeQuestion(_tmpFile, _question):
    with open(_tmpFile, 'a') as _file:
        _file.write(_question)
    _file.close()


def writeAnswers(_tmpFile, _answers):
    with open(_tmpFile, 'a') as _file:
        _file.write('\n\n Answers \n\n')
        for _answer in _answers:
            _file.write(_answer + "\n")
    _file.close()


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Use v9 or v10 for argument")
        exit()

    if sys.argv[1] not in ["v9", "v10"]:
        print("Use v9 or v10 for argument")
        exit()

    _versionCEH = sys.argv[1]
    _url = "https://exampracticetests.com/eccouncil/ceh-" + _versionCEH + "/"
    _tmpFile = _versionCEH + ".txt"

    _html = getHTMLCode(_url)
    _content = _html.find('div', class_='entry-content')
    _questions = _content.find_all('a', text=re.compile('Q[0-9]+'))

    _dataAnswers = []
    initFile(_tmpFile, len(_questions), _versionCEH)

    print("\n\t\t :: Found %d questions :: \n" % len(_questions))

    for _question in _questions:

        print("Getting question && answer =>", _question.getText(), end="\r")

        if 'http' in _question['href']:
            _urlQuestion = _question['href']
        else:
            _urlQuestion = _url + _question['href']

        _html = getHTMLCode(_urlQuestion)

        try:
            _correctAnswerText = _html.find('div', class_='answer')
            _questionText = _html.find('div', class_='question', recursive=True)
            _questionText = re.sub(_regexAnswers, '', _questionText.getText())
            _answersText = re.findall(_regexAnswers, _html.getText())
            _dataAnswers.append("[" + _question.getText() + "] " + _correctAnswerText.getText())

            writeQuestion(_tmpFile, "\n[" + _question.getText() + "] " + _questionText + "\n")

            for _answer in _answersText[0]:
                if len(_answer) > 1:
                    writeQuestion(_tmpFile, _answer + "\n")

        except Exception as e:
            pass

    writeAnswers(_tmpFile, _dataAnswers)
    print("\n\n\t\t   :: File saved :: \n")

# https://exampracticetests.com/eccouncil/ceh-v10/
# 12-50v10.free.draindumps.2020-jan-01.by.francis.557q.vce.pdf.html
