from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import itertools
from matplotlib import dates

####################################################
# User should provide a dataset dictionary
#     key : Item Group Names, will show on y-axis
#     value : list of milestones or tasks
#         - milestone, ['Event Name', 'Date']
#         - tasks, ['Task Name', 'Start Date', 'End Date']
####################################################
dataset = {
        'Department A' : [
            ['Plan Delivery', '2021-9-26'],
            ['Communication 1', '2021-10-29'],
            ['Resource Prepare', '2021-7-26'],
            ['Deliver 1', '2021-10-20'],
            ['Deliver 2', '2021-12-14'],
            ['Final Delivery', '2022-4-20'],
        ],
        'Department B' : [
            ['Experiment', '2021-4-1', '2021-8-2'],
            ['Result 1', '2021-6-15'],
            ['Result 2', '2021-7-28']
        ],
        'Department C' : [
            ['Product Launch Process', '2022-2-10', '2022-6-11'],
            ['RC1', '2022-2-10'],
            ['RC2', '2022-5-28']
        ]
}

color_bg = 'grey'
markSize = 8

categoryHeight = 20

ProperDateInterval = 45

refDate = "2021-1-1"

def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))

def format_xaxis(fig):
    """
    """
    years = dates.YearLocator(1, month=1, day=1)
    months = dates.MonthLocator(bymonthday=15, interval=1)
    dfmt = dates.DateFormatter('%Y')
    dfmt1 = dates.DateFormatter('%b')

    [i.xaxis.set_major_locator(years) for i in fig.axes]
    [i.xaxis.set_minor_locator(months) for i in fig.axes]
    [i.xaxis.set_major_formatter(dfmt) for i in fig.axes]
    [i.xaxis.set_minor_formatter(dfmt1) for i in fig.axes]
    [i.get_xaxis().set_tick_params(which='major', pad=15, length=0)
      for i in fig.axes]
    [i.get_xaxis().set_tick_params(which='minor', length=0)
      for i in fig.axes]

    for t in fig.axes:
         for tick in t.xaxis.get_major_ticks():
              tick.label1.set_horizontalalignment('center')
         for label in t.get_xmajorticklabels():
             label.set_rotation(0)
             label.set_weight('bold')
             label.set_fontsize('large')
         for label in t.xaxis.get_minorticklabels():
             label.set_fontsize('small')

def format_yaxis(ax, categories):
    """
    """
    categories = list(categories)
    ymax = len(categories) * categoryHeight
    ax.set_ylim([0, ymax])
    ySpans = list(range(0, ymax + 1, categoryHeight))
    yMarkerLocs = [categoryHeight * i + categoryHeight/2 for i in range(len(categories))]
    # yMarkerLocs = [10, 30, 50, 70, 90, 110]
    # ySpans = [0, 20, 40, 60, 80, 100, 120]
    spanList = pairwise(ySpans)
    for span in spanList:
        ax.axhspan(span[0], span[1] - 1, facecolor=color_bg, alpha=0.1)
    # yLabels = ["SDK Release", "TSN Release", "Tool Release", "Header Release", "HW", "DOC"]
    ax.set_yticks(yMarkerLocs)
    ax.set_yticklabels(reversed(categories))
    ax.get_yaxis().set_tick_params(length=0)


def months_in_range(start_date, end_date):
    """
    Get the last day of every month in a range between two datetime values.
    Return a generator
    """
    start_month = start_date.month - 1
    end_months = (end_date.year - start_date.year) * 12 + end_date.month + 1

    for month in range(start_month, end_months + 1):
        # Get years in the date range, add it to the start date's year
        year = (month - 1) // 12 + start_date.year  # '//' for exact divide
        month = (month - 1) % 12 + 1
        yield datetime(year, month, 1)  # yield gives a generator function

def add_task(ax, task, yPos, width, color):
    """
    """
    startTime = datetime.strptime(task[1], "%Y-%m-%d")
    endTime = datetime.strptime(task[2], "%Y-%m-%d")
    name = task[0]
    ax.broken_barh([(startTime, endTime - startTime)], (yPos-width/2, width), facecolors=(color))
    ax.text(endTime, yPos + 1, name, size = markSize, ha="left", va="center", weight = "bold")
    startAbbr = startTime.strftime("%b %d")
    endAbbr = endTime.strftime("%b %d")
    ax.text(endTime, yPos - 1, startAbbr + ' ~ ' + endAbbr, ha="left", va="center", size = markSize)

def add_mileStone(plt, milestone, yPos, color):
    """
    """
    mileStoneTime = datetime.strptime(milestone[1], "%Y-%m-%d")
    name = milestone[0]
    markerline, stemlines, baseline = plt.stem([mileStoneTime], [yPos])
    plt.setp(stemlines, linewidth=0.3, linestyle='dotted')    # python style
    plt.setp(baseline, linewidth=0)
    plt.setp(markerline, markersize=10, marker=9, color=color)
    plt.text(mileStoneTime, yPos + 1, name, ha="right", va="center", size = markSize, weight = "bold")
    plt.text(mileStoneTime, yPos - 1, mileStoneTime.strftime("%b %d"), ha="right", va="center", size = markSize)

######
# Find Start End
######
def findStartEnd(dataset):
    """
    """
    key = list(dataset.keys())[0]
    projStart = datetime.strptime(dataset[key][0][1], "%Y-%m-%d")
    projEnd = datetime.strptime(dataset[key][0][len(dataset[key][0])-1], "%Y-%m-%d")
    for key in dataset.keys():
        for item in dataset[key]:
            curStart = datetime.strptime(item[1], "%Y-%m-%d")
            curEnd = datetime.strptime(item[len(item)-1], "%Y-%m-%d")
            if curStart < projStart:
                projStart = curStart
            if curEnd > projEnd:
                projEnd = curEnd
    projStart = projStart - relativedelta(months=1)
    projStart = projStart.replace(day=1)
    projEnd = projEnd + relativedelta(months=1)
    nextMonth = projEnd.replace(day=28) + timedelta(days=4)
    projEnd = nextMonth - timedelta(days=nextMonth.day)
    return projStart, projEnd

########
# add item, either milestone or task
########
def add_item(plt, ax, item, yPos):
    """
    """
    if (len(item) == 2):
        # milestone
        add_mileStone(plt, item, yPos, "cornflowerblue")
    elif (len(item) == 3):
        # task
        add_task(ax, item, yPos, 2, "cornflowerblue")
#######
# drawList
#######
def drawList(plt, ax, itemList, baseline, height):
    prevBase = datetime.strptime(refDate, "%Y-%m-%d")
    baseY = baseline + height / 2
    prevAlt1 = datetime.strptime(refDate, "%Y-%m-%d")
    alt1Y = baseline + height / 4
    prevAlt2 = datetime.strptime(refDate, "%Y-%m-%d")
    alt2Y = baseline + height * 3 / 4
    for item in itemList:
        currentDate = datetime.strptime(item[1], "%Y-%m-%d")
        if (currentDate - prevBase).days > ProperDateInterval:
            # Base
            add_item(plt, ax, item, baseY)
            prevBase = currentDate
        elif (currentDate - prevAlt1).days > ProperDateInterval:
            # Alt1
            add_item(plt, ax, item, alt1Y)
            prevAlt1 = currentDate
        elif (currentDate - prevAlt2).days > ProperDateInterval:
            # Alt2
            add_item(plt, ax, item, alt2Y)
            prevAlt2 = currentDate
        else:
            print("No place to put the new stuff")

########
# drawDatalist
########
def drawDatalist(plt, ax, datalist, baseline, height):
    """
    """
    tempDict = {}
    for item in datalist:
        tempDict.setdefault(len(item), []).append(item)
    keys = tempDict.keys()
    if (len(keys) == 1):
        # only one group
        key = list(keys)[0]
        itemList = sorted(tempDict[key], key=lambda x:datetime.strptime(x[1], "%Y-%m-%d"))
        drawList(plt, ax, itemList, baseline, height)
    else:
        # both interval and milestone
        tasklist = sorted(tempDict[3], key=lambda x:datetime.strptime(x[1], "%Y-%m-%d"))
        drawList(plt, ax, tasklist, baseline, height/2)
        milestoneList = sorted(tempDict[2], key=lambda x:datetime.strptime(x[1], "%Y-%m-%d"))
        drawList(plt, ax, milestoneList, baseline + height/2, height/2)
    return

##########################################################################################################################################################
#
# Main
#
##########################################################################################################################################################
fig, ax = plt.subplots()

##### Draw Spans
projStart, projEnd = findStartEnd(dataset)
x_spans = months_in_range(projStart, projEnd)
spanList = pairwise(x_spans)
for span in spanList:
    ax.axvspan(span[0], span[1] - timedelta(days=0.5),
               facecolor=color_bg, alpha=0.1)
plt.xlim(projStart, projEnd)
format_xaxis(fig)
format_yaxis(ax, dataset.keys())

##### Iterate datasets
baseline = categoryHeight * len(dataset.keys())
for key in dataset.keys():
    datalist = dataset[key]
    baseline -= categoryHeight
    drawDatalist(plt, ax, datalist, baseline, categoryHeight)


plt.show()

