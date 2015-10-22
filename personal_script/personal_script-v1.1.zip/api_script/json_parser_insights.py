__author__ = 'seshadribt24'

import requests


class JsonParser(object):
    def __init__(self, report_id, token, export_columns, account, action_list, video_view_list, non_action_list,
                 action_values, relevance_score):
        self.report_id = report_id
        self.token = token.strip()
        self.export_columns = export_columns
        self.account = account
        self.action_list = action_list
        self.video_view_list = video_view_list
        self.non_action_list = non_action_list
        self.action_values = action_values
        self.relevance_score = relevance_score

    global write_to_csv

    write_to_csv = []  # holds the data to be written to csv

    def parser(self):
        global write_to_csv

        url = 'https://graph.facebook.com/v2.3/' + self.report_id + '/insights?access_token=' + self.token

        print 'url with data: ', url
        data = requests.get(url)
        json_response = data.json()

        data = json_response['summary']

        temp = []
        action_list = self.action_list
        non_action_list = self.non_action_list
        action_value_list = self.action_values

        for value in non_action_list:
            try:
                temp.append(data[value.strip()].encode('utf-8', 'ignore'))
            except:
                temp.append(data[value.strip()])

        relevance_score = self.relevance_score
        if relevance_score != 0:
            for score_element in relevance_score:
                try:
                    temp.append(data['relevance_score'][score_element])
                except:
                    temp.append('0')

        if action_list != 0:
            actions_dict = {}
            for element in data['actions']:
                actions_dict[element['action_type']] = element['value']

            for action in action_list:
                try:
                    temp.append(actions_dict[action])
                except:
                    temp.append('0')

        if action_value_list != 0:
            action_value_dict = {}
            for element in data['action_values']:
                action_value_dict[element['action_type']] = element['value']

            for action in action_value_list:
                try:
                    temp.append(action_value_dict[action])
                except:
                    temp.append('0')

        video_view_list = self.video_view_list
        if video_view_list != 0:
            for action in video_view_list:
                try:
                    temp.append(actions_dict[action])
                except:
                    temp.append('0')

        write_to_csv.append(temp)
        return [write_to_csv]
