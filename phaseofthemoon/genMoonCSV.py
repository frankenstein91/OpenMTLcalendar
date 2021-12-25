from datetime import timedelta, date
import ephem
import csv
import argparse

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="the year to use",type=int)
    args = parser.parse_args()

    start_date = date(args.year, 1, 1)
    end_date = date(args.year+1, 1, 1)
    moon = []
    first = True
    lunationlast = None
    for single_date in daterange(start_date, end_date):
        nnm = ephem.next_new_moon(single_date)
        pnm = ephem.previous_new_moon(single_date)
        lunation = (ephem.Date(single_date) - pnm) / (nnm - pnm)
        lunation = int(lunation / 0.25)

        if lunation == 1:
            lunation = 0
        if first:
            first = False
            moon.append([single_date.strftime("%Y-%m-%d"),str(lunation), ""])
            lunationlast = lunation
        else:
            if not lunationlast == lunation:
                moon.append([single_date.strftime("%Y-%m-%d"), str(lunation), ""])
                lunationlast = lunation
    moontext = [["date","day_text","note"]]
    moontext.extend(moon)
    with open(f'moon.csv', 'w', newline='') as moon_file:
        moon_writer = csv.writer(moon_file, delimiter=";")
        for moons in moontext:
            print(moons)
            if moons[1] == "0":
                moon_writer.writerow([moons[0], "\\NewMoon", moons[2]])
            elif moons[1] == "1":
                moon_writer.writerow([moons[0], "\\FirstQuarter", moons[2]])
            elif moons[1] == "2":
                moon_writer.writerow([moons[0], "\\FullMoon", moons[2]])
            elif moons[1] == "3":
                moon_writer.writerow([moons[0], "\\LastQuarter", moons[2]])







