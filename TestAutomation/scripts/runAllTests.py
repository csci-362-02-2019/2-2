import os, subprocess
import importlib.util
from oracle_exegen import oracle_exegen

# MAIN TEST SCRIPT
# TO RUN THIS SCRIPT, CD TO 'TestAutomation',
# then execute the command 'python3 scripts/runAllTests.py

def reportHeader():
    header = '''
    <table border="2" width="100%">
        <tr align="center">
            <th colspan="9">Testing Report</th>
        <tr>
            <th> Test # </th>
            <th> Pass/Fail </th>
            <th> Test ID </th>
            <th> Requirements Being Tested </th>
            <th> Component </th>
            <th> Method </th>
            <th> Input </th>
            <th> Expected Output </th>
            <th> Actual Output </th>
        </tr>\n'''
    return header

report = os.path.join('.', 'reports', 'testReport.html')
testcases = os.path.join('.', 'testCases')
testcaseexecutable = os.path.join('.', 'testCasesExecutables', 'test.js')

with open(report, "w") as htmlfile:
    htmlfile.write('''<!DOCTYPE html>\n
    <html lang="en-US" style="height: 100%;">\n
    <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Testing Report</title>\n''')

    htmlfile.write(reportHeader())
    lineCount = 0

    # set maxTableSize to -1 for no limit
    maxTableSize = -1
    for testcase in sorted(os.listdir(testcases)):
        print('\ntesting', testcase)
        oracle_exegen(os.path.join(testcases, testcase),testcaseexecutable)

        print('executing test')
        proc = subprocess.Popen('npm run oracle 2>&1', shell=True,stdout=subprocess.PIPE)

        lines = proc.stdout.readlines()
        expectval = lines[-3].decode('utf-8').strip('\n').strip('\r').strip()
        returnval = lines[-2].decode('utf-8').strip('\n').strip('\r').strip()
        resval = lines[-1].decode('utf-8').strip('\n').strip('\r')
        print('results:', resval)
        print('expectval:', expectval)
        print('returnval:', returnval)

        casefile = open(os.path.join(testcases, testcase),"r")
        lines = casefile.readlines()
        casefile.close()

        print('writing to report')
        reportLine='\t\t<tr>\n\t\t\t<td>'+str(lineCount+1)+'</td>\n\t\t\t<td>'
        if (lineCount % maxTableSize == 0 and lineCount != 0 and maxTableSize != -1):
            reportLine='\t</table>\n\t\t<br>'+reportHeader()+reportLine

        if resval == "Pass":
            reportLine += 'Pass &#x2705</td>\n'
        elif resval == "Fail":
            reportLine += 'Fail &#x26D4</td>\n'
        else:
            reportLine += 'Error</td>\n'

        for input in lines:
            elementsList = input.split(':')
            element = elementsList[1].strip()
            reportLine += '\t\t\t<td>' + element + '</td>\n'

        reportLine += '\t\t\t<td>' + returnval.strip() + '</td>\n'
        reportLine += '\t\t</tr>\n'
        htmlfile.write(reportLine)
        lineCount += 1
        print(testcase, 'complete')

    htmlfile.write('\t\t</table>\n\t</head>')
    print("\nall tests done")

print('opening report')
try: subprocess.call(['xdg-open', report])
except:
    try: os.startfile(report)
    except: pass