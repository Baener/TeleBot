import requests, csv
from bs4 import BeautifulSoup

URL = "https://rostov-na-donu.restate.ru/poisk/?dealid=2&region=39335&object=sareas-1&input-search=&price_to=&pricetype=1&frompodbor2021=1&o=0&page="

meanAreaStudio = [0, 0]
meanAreaOne = [0, 0]
meanAreaTwo = [0, 0]
meanAreaThree = [0, 0]
meanPricePerAreaW = [0, 0]
meanPricePerArea = [0, 0]

file = []

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Referer": "https://rostov-na-donu.restate.ru/"
}

def GetParcing():
    pars(URL)
    print(meanAreaStudio)
    print(meanAreaOne)
    print(meanAreaTwo)
    print(meanAreaThree)
    print(meanPricePerAreaW)
    print(meanPricePerArea)
    return [meanAreaStudio[1], meanAreaOne[1], meanAreaTwo[1], meanAreaThree[1], meanPricePerAreaW[1]]

def pars(url):
    global meanAreaStudio
    global meanAreaOne
    global meanAreaTwo
    global meanAreaThree
    global meanPricePerAreaW
    global meanPricePerArea

    pastId = 0
    
    num = 1
    while True:
        print(num)
        urlpage = url + str(num)
        num += 1
        response = requests.get(url = urlpage, headers = headers)
        headers['Referer'] = urlpage
        soup = BeautifulSoup(response.text, "lxml")
        idCard = int(soup.find("div", class_="sri")["data-id"])
        if idCard == pastId:
            break
        else:
            pastId = idCard
        cards = soup.find_all("div", class_="sri__content")
        for i in range(len(cards)):
            info = cards[i].find("p", class_="sri__header link").text.replace("\n","").replace("\xb2","").split(", ")
            area = 0
            if ('м' in info[len(info) - 1]):
                area = float(info[len(info) - 1][0:-2])
            elif('м' in info[len(info) - 2]):
                area = float(info[len(info) - 2][0:-2])
            else:
                break
            if info[0][0].isdigit() or info[0] == "Студия" or info[0] == "Квартира":
                if info[0] == "Студия" or info[0] == "Квартира":
                    meanAreaStudio[0] += 1
                    meanAreaStudio[1] = (meanAreaStudio[1] * (meanAreaStudio[0] - 1) + area) / meanAreaStudio[0]
                elif int(info[0][0]) == 1:
                    meanAreaOne[0] += 1
                    meanAreaOne[1] = (meanAreaOne[1] * (meanAreaOne[0] - 1) + area) / meanAreaOne[0]
                elif int(info[0][0]) == 2:
                    meanAreaTwo[0] += 1
                    meanAreaTwo[1] = (meanAreaTwo[1] * (meanAreaTwo[0] - 1) + area) / meanAreaTwo[0]
                elif int(info[0][0]) == 3:
                    meanAreaThree[0] += 1
                    meanAreaThree[1] = (meanAreaThree[1] * (meanAreaThree[0] - 1) + area) / meanAreaThree[0]
            price = float(cards[i].find("p", class_="sri__price").text.replace("\n","").replace("₽","").replace(" ",""))
            #Средневзвешенное
            meanPricePerAreaW[0] += area
            meanPricePerAreaW[1] = (meanPricePerAreaW[1] * (meanPricePerAreaW[0] - area) + price) / meanPricePerAreaW[0]
            #Среднее
            meanPricePerArea[0] += 1
            meanPricePerArea[1] = (meanPricePerArea[1] * (meanPricePerArea[0] - 1) + (price / area)) / meanPricePerArea[0]

#if __name__ == "__main__":
    #GetParcing()

