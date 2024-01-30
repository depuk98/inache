from datetime import timedelta, date
import datetime
from accounts.models import HolidayCalendar
from dateutil.rrule import rrule, DAILY

two_four_sat = set(range(8, 15)) | set(
    range(22, 29))  # for any month, second and fourth saturday falls in (8-14) and (22-28) dates


def working_days(start_date, end_date, factory):
    list = []
    for i in range((end_date - start_date).days + 1):
        date = (start_date + timedelta(days=i))
        # iterating through dates, excluding sunday which is weekday "6" and saturdays which falls in above said dates
        list.append(not ((date.weekday() in [6]) or (date.weekday() in [
                    5] and date.day in two_four_sat) or (holidayCheck(date,factory))))

    # print(list)
    # so, the list contains true for working days and false for non-working days, sum of list give number of true values i.e, working days
    return sum(list)


def holidayCheck(Date,Factory):
    holiday = HolidayCalendar.objects.filter(
        startDate__date__lte=Date, endDate__date__gte=Date, Factory=Factory)
    return holiday.exists()

def holidayCheckFactory(Date, factory):
    holiday = HolidayCalendar.objects.filter(Factory=factory,
        startDate__date__lte=Date, endDate__date__gte=Date)
    return holiday.exists()

def is_working_day(date, factory):
    if ((date.weekday() in [6]) or (date.weekday() in [5] and date.day in two_four_sat) or (holidayCheck(date,factory))):
        return False
    else:
        return True


def convertStringToDate(Date):
    timestamp_str = Date  # "2023-05-15 15:33:09.681047+05:30",
    format_str = '%Y-%m-%d %H:%M:%S.%f%z'
    Date_datetime = datetime.datetime.strptime(timestamp_str, format_str)
    Date = Date_datetime.date()
    return Date


def convertDateStringToDate(Date):
    timestamp_str = Date  # "2023-05-15 15:33:09.681047+05:30",
    format_str = '%Y-%m-%d %H:%M:%S%z'
    Date_datetime = datetime.datetime.strptime(timestamp_str, format_str)
    Date = Date_datetime.date()
    return Date


def convertDatestringToDate(Date):
    date_str = Date  # "2023-05-15"
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj


def timeFrameCheck(startDate, endDate, factory):
    startDate = convertStringToDate(startDate)
    endDate = convertStringToDate(endDate)
    return working_days(startDate, endDate, factory)


def pastDateCheck(startDate, endDate):
    startDate = convertStringToDate(startDate)
    endDate = convertStringToDate(endDate)
    if startDate < date.today() or endDate < date.today():
        return True
    else:
        return False


def pastDateStringCheck(startDate, endDate):
    startDate = convertDateStringToDate(startDate)
    endDate = convertDateStringToDate(endDate)
    if startDate < date.today() or endDate < date.today():
        return True
    else:
        return False


def startEndCheck(startDate, endDate):
    startDate = convertStringToDate(startDate)
    endDate = convertStringToDate(endDate)
    if startDate > endDate:
        return True
    else:
        return False


def weekDayName(startDate, endDate):
    list = []
    firstLast = []
    for i in range((endDate - startDate).days + 1):
        Date = (startDate + timedelta(days=i))
        list.append(Date.strftime('%A'))
    firstLast.append(list[0])
    firstLast.append(list[-1])
    if list[0] == list[-1]:
        return list[0]
    return " - ".join(firstLast)


def getMonthName(string):
    date_obj = datetime.datetime.strptime(string, "%Y-%m")
    month_name = date_obj.strftime("%B")
    return month_name


def convertDatetimeToHolidayFormat(Datetime):
    date_string = Datetime.strftime("%m/%d/%Y")
    return date_string


def programCheck(Date, factory):
    Date_str = Date
    format_str = '%Y-%m-%d %H:%M:%S.%f%z'
    Date_datetime = datetime.datetime.strptime(str(Date_str), format_str)
    Date = Date_datetime.date()
    Today = datetime.date.today().date()
    working_days = last_three_working_days(Date.year, Date.month, factory)
    grace_days = first_two_working_days(Today.year, Today.month, factory)
    if (Date in working_days) and (Today in grace_days):
        return True
    else:
        return False


def last_three_working_days(year, month, factory):
    last_day = datetime.date(year, month, 1)
    while last_day.month == month:
        last_day += datetime.timedelta(days=1)
    last_day -= datetime.timedelta(days=1)

    working_days = []
    two_four_sat = set(range(8, 15)) | set(range(22, 29))
    while len(working_days) < 3:
        if ((last_day.weekday() in [6]) or (last_day.weekday() in [5] and last_day.day in two_four_sat) or (holidayCheck(last_day, factory))) == False:
            working_days.append(last_day)
        last_day -= datetime.timedelta(days=1)

    return working_days


def first_two_working_days(year, month, factory):
    first_day = datetime.date(year, month, 1)
    working_days = []
    two_four_sat = set(range(8, 15)) | set(range(22, 29))
    while len(working_days) < 2:
        if ((first_day.weekday() in [6]) or (first_day.weekday() in [5] and first_day.day in two_four_sat) or (holidayCheck(first_day, factory))) == False:
            working_days.append(first_day)
        first_day += datetime.timedelta(days=1)
    return working_days

# takes start date, no. of working days required


def workingDaysAddition(Date, input, factory):
    # number of days to be added
    add = 0
    # number of working days needed
    workingDays = 0
    startDate = Date
    # loops iterates through subsequent dates and checks whether its a working day
    while workingDays < input:
        Date = Date + timedelta(days=1)
        if ((Date.weekday() in [6]) or (Date.weekday() in [5] and Date.day in two_four_sat) or (holidayCheck(Date, factory))) == False:
            workingDays += 1
        add += 1
    # once its reached required number of working days, it adds the number of days to start date
    return startDate + timedelta(days=add)

def workingHoursAddition(Date, remains, factory):
    total_hours = 0
    remains = remains

    # checks if given date is working day
    if is_working_day(Date, factory):
        startDate= Date
    # if not, take the next working day and count from 00:00
    else:
        startDate = workingDaysAddition(Date,1, factory)
        startDate = startDate.replace(hour=0, minute=0, second=0)
   
    startDate.replace(microsecond=0)
    start_hour = split_date_time(startDate)[1]
    end_hour = datetime.time(23, 59, 59)
    #calculate number of hours
    total_hours = calculate_working_hours(start_hour, end_hour)

    # if the day has more hours than required, just add sufficient hours to date and return duedate
    if total_hours > remains:
        return startDate + timedelta(hours=remains)
    # if hours are not sufficient, go to next working day, add the remaining hours left from previous day and return duedate
    else:
        remains = remains - total_hours
        startDate = workingDaysAddition(startDate,1,factory)
        startDate = startDate.replace(hour=0, minute=0, second=0)
        return workingHoursAddition(startDate,remains,factory)


def date_range(start_date, end_date):
    return rrule(DAILY, dtstart=start_date, until=end_date)


def count_working_hours(start_date, end_date, factory):
    total_hours = 0
    start_timestamp = split_date_time(start_date)[1]
    end_timestamp = split_date_time(end_date)[1]

    for day in date_range(start_date, end_date):
        if (start_date.date() > end_date.date()):
            print("end date should be greater than start date")
            break
        elif is_holiday(day,factory):
            continue
        elif (start_date.date() == end_date.date()):
            return calculate_working_hours(start_timestamp, end_timestamp)
        elif (day == start_date.replace(microsecond=0)):
            start_hour = start_timestamp
            end_hour = datetime.time(23, 59, 59)
            # print('first')
        elif (day == end_date.replace(microsecond=0)):
            start_hour = datetime.time(0, 0, 0)
            end_hour = end_timestamp
            # print('last')
        elif ((day != start_date.replace(microsecond=0)) and (day != end_date.replace(microsecond=0))):
            start_hour = datetime.time(0, 0, 0)
            end_hour = datetime.time(23, 59, 59)
            # print('middle')
        # print(start_hour,end_hour)
        total_hours += calculate_working_hours(start_hour, end_hour)
    return total_hours


def split_date_time(date_time_str):
    dt = datetime.datetime.strftime(date_time_str, '%Y-%m-%d %H:%M:%S')
    date = datetime.datetime.strftime(date_time_str, '%Y-%m-%d')
    time = datetime.datetime.strftime(date_time_str, '%H:%M:%S')
    return date, time


def is_holiday(date, factory):
    two_four_sat = set(range(8, 15)) | set(range(22, 29))
    return ((date.weekday() in [6]) or (date.weekday() in [5] and date.day in two_four_sat) or (holidayCheck(date, factory)))


def calculate_working_hours(start_time, end_time):
    start_time = datetime.datetime.strptime(str(start_time), "%H:%M:%S")
    end_time = datetime.datetime.strptime(str(end_time), "%H:%M:%S")
    return (end_time - start_time).total_seconds() / 3600


# converting date to string with this "2022-11-30 18:17:16" format
def convertDate(my_date):
    dt = datetime.datetime.fromisoformat(my_date)
    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


# startDate = current_time() - timedelta(days=1)
# endDate = current_time()
# working_hours = count_working_hours(startDate, endDate)
# print(working_hours)  # Output: 19

# 2022-11-30T18:17:16.198647+05:30


def futureDateStringCheck(startDate, endDate):
    startDate = convertDatestringToDate(startDate).date()
    endDate = convertDatestringToDate(endDate).date()
    if startDate > date.today() or endDate > date.today():
        return True
    else:
        return False

def analyticsStartEndCheck(startDate, endDate):
    startDate = convertDatestringToDate(startDate).date()
    endDate = convertDatestringToDate(endDate).date()
    if startDate > endDate:
        return True
    else:
        return False
