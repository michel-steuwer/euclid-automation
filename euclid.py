#!/usr/bin/env python3
"""EUCLID CLI

Usage:
    euclid.py record_attendance
        (-u <username>) (-p <password>) (-s <secure_word>)
        (--student_name=<name> [--date=<date>] --description=<msg> [--notes=<notes>])...

    euclid.py (-h | --help)
    euclid.py --version

Options:
    -h, --help                                      Show this screen.
    -v, --version                                   Show version.
    -u <username>, --username=<username>            EASE username.
    -p <password>, --password=<password>            EASE password.
    -s <secure_word>, --secure_word=<secure_word>   EASE secure word.
    -n <name>, --student_name=<name>                Name of the student.
    -d <date>, --date=<date>                        Date. If not given the date of the current day is used.
    --description=<msg>                             Description of the attendance event.
    --notes=<notes>                                 Optional notes recorded in the attendance event.
"""

from docopt import docopt
from datetime import datetime
from record_attendance import record_attendance

if __name__ == '__main__':
    args = docopt(__doc__, version="EUCLID CLI 1.0")

    if args['record_attendance']:
        names = args["--student_name"]
        dates = args["--date"]
        msgs = args["--description"]
        notes = args["--notes"]
        if len(dates) == 0:
            today = datetime.today().strftime("%d/%b/%Y")
            dates = [today] * len(names)
        if len(notes) == 0:
            notes = [''] * len(names)

        students = []
        for n, d, m, ns in zip(names, dates, msgs, notes):
            students.append({
                "name": n,
                "date": d,
                "description": m,
                "notes": ns
            })

        record_attendance(students, args['--username'], args['--password'], args['--secure_word'])

    print("done")
