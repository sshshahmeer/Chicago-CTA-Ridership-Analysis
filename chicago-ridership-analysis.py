import pandas
import sqlite3
# Outputs provided in the main function.

def add_data_to_database():
    # Answer to Problem 1: The database is 38.9 MB in size
    data = pandas.read_csv("CTA-Ridership-L-Station-Entries-Daily-Totals.csv", names=['station_id','stationname','date','daytype','rides'], skiprows=[0])
    conn = sqlite3.connect("cta.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE daily_ridership_counts (station_id int, stationname text, date text, daytype text, rides int)")

    for i in range(len(data)):
        a = int(data['station_id'][i])
        b = data['stationname'][i]
        c = data['date'][i]
        d = data['daytype'][i]
        e = int(data['rides'][i])
        sql = "INSERT INTO daily_ridership_counts (station_id, stationname, date, daytype, rides) VALUES (:station_id, :stationname, :date, :daytype, :rides)"
        cur.execute(sql, {"station_id":a, "stationname":b, "date":c, "daytype":d, "rides":e})

    conn.commit()
    conn.close()

def avg_monthly_count_uic_halsted():
    date = []
    Jan = []
    Feb = []
    Mar = []
    Apr = []
    May = []
    Jun = []
    Jul = []
    Aug = []
    Sep = []
    Oct = []
    Nov = []
    Dec = []
    conn = sqlite3.connect("cta.db")
    curr = conn.cursor()
    sql = "SELECT date,rides from daily_ridership_counts where station_id=40350"
    dates_and_rides_column = curr.execute(sql)
    all_dates_and_rides = dates_and_rides_column.fetchall()
    for dates_and_rides in all_dates_and_rides:
        date.append(dates_and_rides)
    for i in date:
        month = i[0][0:2]
        rides = i[1]
        if month == "01":
            Jan.append(rides)
        elif month == "02":
            Feb.append(rides)
        elif month == "03":
            Mar.append(rides)
        elif month == "04":
            Apr.append(rides)
        elif month == "05":
            May.append(rides)
        elif month == "06":
            Jun.append(rides)
        elif month == "07":
            Jul.append(rides)
        elif month == "08":
            Aug.append(rides)
        elif month == "09":
            Sep.append(rides)
        elif month == "10":
            Oct.append(rides)
        elif month == "11":
            Nov.append(rides)
        elif month == "12":
            Dec.append(rides)
    print("******************************************")
    print("January:",sum(Jan)/len(Jan))
    print("February:",sum(Feb)/len(Feb))
    print("March:",sum(Mar)/len(Mar))
    print("April:",sum(Apr)/len(Apr))
    print("May:",sum(May)/len(May))
    print("June:",sum(Jun)/len(Jun))
    print("July:",sum(Jul)/len(Jul))
    print("August:",sum(Aug)/len(Aug))
    print("September:",sum(Sep)/len(Sep))
    print("October:",sum(Oct)/len(Oct))
    print("November:",sum(Nov)/len(Nov))
    print("December:",sum(Dec)/len(Dec))
    print("******************************************")

def getWeekday(year, month, day):
    """
    input: integers year, month, day
    output: name of the weekday on that date as a string
    """
    import datetime
    import calendar
    date = datetime.date(year, month, day)
    return calendar.day_name[date.weekday()]

def avg_weekly_count_uic_halsted():
    Mon = []
    Tue = []
    Wed = []
    Thu = []
    Fri = []
    Sat = []
    Sun = []
    conn = sqlite3.connect("cta.db")
    curr = conn.cursor()
    sql = "SELECT date,rides from daily_ridership_counts where station_id=40350"
    dates_and_rides_column = curr.execute(sql)
    all_dates_and_rides = dates_and_rides_column.fetchall()
    for dates_and_rides in all_dates_and_rides:
        year = int(dates_and_rides[0][-4:])
        month = int(dates_and_rides[0][:2])
        day = int(dates_and_rides[0][3:5])
        rides = dates_and_rides[1]
        if getWeekday(year, month, day) == "Monday":
            Mon.append(rides)
        elif getWeekday(year, month, day) == "Tuesday":
            Tue.append(rides)
        elif getWeekday(year, month, day) == "Wednesday":
            Wed.append(rides)
        elif getWeekday(year, month, day) == "Thursday":
            Thu.append(rides)
        elif getWeekday(year, month, day) == "Friday":
            Fri.append(rides)
        elif getWeekday(year, month, day) == "Saturday":
            Sat.append(rides)
        elif getWeekday(year, month, day) == "Sunday":
            Sun.append(rides)
    print("Monday:",(sum(Mon)/len(Mon)))
    print("Tuesday:",(sum(Tue)/len(Tue)))
    print("Wednesday:",(sum(Wed)/len(Wed)))
    print("Thursday:",(sum(Thu)/len(Thu)))
    print("Friday:",(sum(Fri)/len(Fri)))
    print("Saturday:",(sum(Sat)/len(Sat)))
    print("Sunday:",(sum(Sun)/len(Sun)))
    print("******************************************")

def busiest_station():
    rides_per_station = {}
    conn = sqlite3.connect("cta.db")
    curr = conn.cursor()
    sql = "SELECT rides,stationname from daily_ridership_counts"
    rides_and_stationname_columns = curr.execute(sql)
    all_rides_and_stationnames = rides_and_stationname_columns.fetchall()
    for rides_and_stations in all_rides_and_stationnames:
        rides = rides_and_stations[0]
        station = rides_and_stations[1]
        if station in rides_per_station:
            rides_per_station[station] += rides
        else:
            rides_per_station[station] = rides
    Busiest_station = max(rides_per_station, key=rides_per_station.get)
    print("Busiest Station:", Busiest_station)
    print("Total rides:", rides_per_station[Busiest_station])
    print("******************************************")



def main():
    # add_data_to_database()
    avg_monthly_count_uic_halsted()
    """
    OUTPUT
    January: 3907.7758913412563
    February: 4955.733208955224
    March: 4375.134125636672
    April: 4863.619298245614
    May: 2899.1358234295417
    June: 2919.5263157894738
    July: 2877.663701067616
    August: 3518.5681003584227
    September: 5675.288888888889
    October: 5931.137992831541
    November: 5104.498148148148
    December: 2920.8888888888887
    """
    
    avg_weekly_count_uic_halsted()
    """
    OUTPUT
    Monday: 4896.282316442606
    Tuesday: 5322.035233160622
    Wednesday: 5393.282901554404
    Thursday: 5242.0590062111805
    Friday: 5043.746376811594
    Saturday: 1812.1533678756477
    Sunday: 1305.919170984456
    """
    busiest_station()
    """
    OUTPUT
    Busiest Station: Clark/Lake
    Total rides: 94799999
    """

main()
