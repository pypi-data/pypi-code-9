#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os
import requests, sys
from lxml import html
from time import sleep
import json
import datetime

class Scraper:
    def __init__(self, db, session):
        print "Initialized Moodle Scraper"
        self.session = session
        self.db = db

    def loop(self, from_id, to_id, category):
        for i in range(from_id, to_id + 1):
            self.extract(i, category)

    def extract(self, ID, category):

        base_url = "http://moodle.regis.org/user/profile.php?id="
        if category is "course":
            base_url = "http://moodle.regis.org/course/view.php?id="
        # Get the page
        r = self.session.get(base_url + str(ID))  # The url is created by appending the current ID to the base url
        # Parse the html returned so we can find the title
        #print r.text
        parsed_body = html.fromstring(r.text)
        # Get the page title
        title = parsed_body.xpath('//title/text()')
        # Check if page is useful
        if len(title) == 0:
            #print "Bad title"
            return

        if "Test" in title:
            #print "Skipped test entry"
            return

        if ("Error" in title[0].strip()) or ("Notice" in title[0].strip()):
            #print "Error or Notice skipped"
            return

        # COURSE
        title = parsed_body.xpath('//title/text()')[0]
        parts = title.split(": ")
        if parts[0] == "Course":
            name = parts[1]
            ps = name.split(" ")

            teacher = parts[2] if len(parts) > 2 else "Unknown"

            if "Advisement " in name:
                out = {
                    "tID": teacher,
                    "title": name.replace("Advisement ", ""),
                    "mID": ID
                }
                print str(ID)+": Advisement " + out['title'] + " " + str(self.db.advisements.insert_one(out).inserted_id)

            else:
                grade = 13
                for pa in ps:
                    for index, g in enumerate(["I", "II", "III", "IV"]):
                        if g == pa:
                            grade = 9 + index
                    try:
                        grade = int(pa)
                    except ValueError:
                        pass
                courseType = "class"
                if "Club" in name or "Society" in name:
                    courseType = "club"

                if "REACH" in name or "Reach" in name:
                    courseType = "reach"

                out = {
                    "full": title,
                    "courseType": courseType,
                    "mID": ID,
                    "title": name,
                    "students": [],
                    "grade": grade
                }
                print str(ID)+": Course " + str(self.db.courses.insert_one(out).inserted_id)
        else:
            # USER
            name_parts = parsed_body.xpath('//title/text()')[0].split(":")[0].split(", ") if len(
                parsed_body.xpath('//title/text()')) > 0 else ['Unknown']
            department = parsed_body.xpath('//dl/dd[1]/text()')
            if len(department) == 0:
                return
            else:
                department = department[0]
            class_as = parsed_body.xpath('//dl/dd[2]/a')

            classes = []
            for a in class_as:
                classes.append(int(a.get("href").split("id=")[1]))

            f = department[0]
            try:
                int(f)
                userType = "student"
            except ValueError:
                userType = "teacher"

            if department.startswith("REACH"):
                userType = "other"

            picsrc = "/images/person-placeholder.jpg"

            for img in parsed_body.xpath('//img[@class=\'userpicture\']'):
                picsrc = img.get("src")

            collect = self.db.courses
            courses = []

            intranet = self.session.get("http://intranet.regis.org/infocenter/default.cfm?FuseAction=basicsearch&searchtype=namewildcard&criteria="+name_parts[0]+"%2C+"+name_parts[1]+"&[whatever]=Search")
            intrabody = html.fromstring(intranet.text)

            schedule = "<h2>Not Found</h2>"

            if userType == "student":
                style="float:left;width:200px;"
            else:
                style="float:left; width:200px;"

            if userType == "student":
                if classes:
                    adv = self.db.advisements.find_one({"mID": classes[0]})
                    if adv:
                        department = adv['title']

            search_results = intrabody.xpath('//div[@style="'+style+'"]/span[1]/text()')
            #print search_results
            if len(search_results) == 0:
                print str(ID)+": Found on Moodle but not the Intranet. Disregarding."
                return # should people found only on Moodle be included?

            #print "Intranet found "+str(len(search_results))+" search results for", name_parts
            for result in search_results:
                index = search_results.index(result)
                name_p = result.encode('utf-8').split(", ")
                intranet_dep = name_p[1].split(" ")[1].replace("(", "").replace(")", "")

                first_name = name_p[1].split(" ")[0]
                last_name = name_p[0]
                #print "Attempting to match "+ str([name_parts[0], name_parts[1], department])+" with " + str([last_name, first_name, intranet_dep])
                if [last_name, first_name] == name_parts:
                    if userType == "student":
                        if intranet_dep == department:
                            #print "Yup!"
                            break
                    else:
                        #print "Yup!"
                        break
                #print "Nope"

            email = intrabody.xpath('//div[@style="'+style+'"]/span[2]/a/text()')[index]
            #print email
            username = str(email).replace("@regis.org", "").lower()

            pic_elm = intrabody.xpath('//div[@style="'+style+'"]/a')[index]
            code = pic_elm.get("href").split("/")[-1].replace(".jpg", "")

            if userType == "student":
                style="float:left;width:200px;"
                scheduleurl = "http://intranet.regis.org/infocenter/"
            else:
                style="float:left; width:200px;"
                scheduleurl = "http://intranet.regis.org/infocenter/default.cfm?StaffCode="+code

            htmlschedulereq = self.session.get(scheduleurl)
            htmls = html.fromstring(htmlschedulereq.text)
            if len(htmls.xpath('//div[@id="main"]/table[4]')) > 0:
                schedule = html.tostring(htmls.xpath('//div[@id="main"]/table[4]')[0])

            try:
                if userType == "student":
                    out = {
                        "mID": ID,
                        "firstName": name_parts[1],
                        "lastName": name_parts[0],
                        "username": username,
                        "code": code,
                        "mpicture": picsrc,
                        "ipicture": pic_elm.get("href"),
                        "schedule": schedule,
                        "email": username + "@regis.org",
                        "advisement": department,
                        "courses": courses,
                        "sclasses": classes,
                    }
                    newID = self.db.students.insert_one(out).inserted_id
                    print str(ID)+": Student " + username + " in Advisement " + department + " with Student ID "+code+" in "+str(len(classes))+" courses"
                    if classes:
                        self.db.advisements.update_one({"mID": classes[0]}, {"$push": {"students": newID} } )
                        for c in classes: # C IS A MOODLE ID
                            course = collect.find_one({"mID": c})
                            if course:
                                cID = course['_id']
                                collect.update_one({"mID": c}, {"$push": {"students": newID}})
                                self.db.students.update_one({"_id": newID}, {"$push": {"courses": cID}})

                else:
                    print str(ID)+": Staff Member " + username + " of the " + department + " Department with Staff ID "+code+" in "+str(len(classes))+" courses"
                    out = {
                        "userType": userType,
                        "mID": ID,
                        "image": picsrc,
                        "code": code,
                        "ipicture": pic_elm.get("href"),
                        "department": department,
                        "firstName": name_parts[1],
                        "lastName": name_parts[0],
                        "schedule": schedule,
                        "username": username,
                        "email": email,
                        "sclasses": classes,
                        "courses": courses
                    }
                    newID = self.db.teachers.insert_one(out).inserted_id
                    #print "Teacher " + str(ID) + ": " + str(newID)
                    for c in classes:
                        course = collect.find_one({"mID": c})
                        if course:
                            if name_parts[0] in course["full"]:
                                #print "COURSE:", course['title']
                                collect.update_one({
                                  '_id': course['_id']
                                },{
                                  '$set': {
                                    'teacher': newID
                                  }
                                }, upsert=False)
                            self.db.teachers.update_one({"_id": newID}, {"$push": {"courses": course['_id']}})
                        adv = self.db.advisements.find_one({"mID": c})
                        if adv:
                            self.db.advisements.update_one({
                              'mID': c
                            },{
                              '$set': {
                                'teacher': newID
                              }
                            })
                            #print "Set Teacher "+str(ID)+" as Advisor of "+adv['title']

            #raw_input("Continue?")
            except Exception as e:
                print e
