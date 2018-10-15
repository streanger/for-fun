import os
import sys
import re
import requests

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)    
    
def levels(totalPoints):
    levelsDict = {
        'Computer Illiterate':range(0x000, 0x010 + 1),
        'a User':range(0x011, 0x040 + 1),
        'an Operator':range(0x041, 0x080 + 1),
        'a Nerd':range(0x081, 0x0C0 + 1),
        'a Hacker':range(0x0C1, 0x100 + 1),
        'a Guru':range(0x101, 0x180 + 1),
        'a Wizard':range(0x181, 0x200 + 1),
    }
    for key, value in levelsDict.items():
        if totalPoints in value:
            return key
    else:
        return "looser"
        
        
if __name__ == "__main__":
    result = requests.get("http://www.mit.edu/people/mjbauer/Purity/hackpure.html")
    content = [item.strip() for item in remove_html_tags(result.text).split('\n')]
    totalPoints = 0
    allQuestions = 0
    for line in content:
        if line.startswith("0") and not line.startswith("0x"):
            allQuestions += 1
            ask = input("{} (yes/no)\t".format(line))
            if ask.lower() == 'yes':
                totalPoints += 1
        else:
            if line:
                input('\t' + line + '\t')
    print("\nYour total score is: {0:#05x}/{1:#05x} ({0}/{1})".format(totalPoints, allQuestions))        
    yourLevel = levels(totalPoints)
    print('You are: "{}"\n'.format(yourLevel))
