
def calc_profit(dailyProfit, peopleNumber):
    ''' dailyProfit in seconds
    peopleNumber who uses solution
    working days in 2018: 250
    working hours in 2018: 2000
    yearProfit in hours
    '''
    workingDays = 250
    yearProfit = dailyProfit*250*peopleNumber/3600
    return yearProfit
    
    
if __name__ == "__main__":
    dailyProfit = 20
    peopleNumber = 30
    out = calc_profit(20, 30)
    print("daily profit per one person: {} [s]\nnumber of people: {}\ntotal time profit during one year: {} [h]".format(dailyProfit,
                                                                                                                      peopleNumber,
                                                                                                                      round(out,2)))
