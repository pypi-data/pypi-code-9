#!/usr/bin/env python
# -*- coding: utf-8 -*-
from student import Student
from room_file import RoomFile
import logging
import codecs
import re
import shutil
import datetime


logging.basicConfig(filename='errors.log', level=logging.ERROR, filemode="w")

class FileParser:

    STUDENT_PATTERN = re.compile(ur'''(?P<id>\d{9})\s*(?P<lastname>[א-ת'()\s]+)(?<=\s)(?P<firstname>[א-ת()']+)''', re.UNICODE)


    def __init__(self, raw_file):
        self.raw_file = raw_file
        self.found_errors = False

    def create_room_auth_file(self, room_number, file_path):
        roomfile = RoomFile(room_number, file_path)
        with codecs.open(self.raw_file, "r", "cp1252") as student_file:
            for line in student_file:
                student = self.parse_line(line)
                try:
                    row = (student.firstname, student.lastname,
                            student.student_id, room_number, "Add")
                    roomfile.worksheet.append(row)
                except (AttributeError, TypeError) as e:
                    print "error adding line %s for line %s" % (e,row)
        roomfile_name = roomfile.filename
        time_now_string = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
        #shutil.copy2(roomfile_name, roomfile_name + "_" + time_now_string + ".xlsx")
        roomfile.workbook.save(roomfile_name)

    def parse_line(self, line):
        encoded_line = line.encode("cp1252").decode('cp1255', errors='replace')
        joined_line = " ".join(encoded_line.split())
        match = FileParser.STUDENT_PATTERN.search(joined_line)
        if not match:
            self.found_errors = True
            logging.error("ParseError: can't parse line: %s" % joined_line)
        else:
            return Student(match.group('id'),
                    match.group('firstname')[::-1], match.group('lastname')[::-1])

