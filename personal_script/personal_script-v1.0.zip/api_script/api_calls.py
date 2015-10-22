__author__ = 'seshadribt24'
import requests
from json_parser_insights import JsonParser
import csv
import time


class ApiFiltered(object):
    def __init__(self, token='', ad_account='', campaign_id='', adset_id='', adgroup_id='', start='', end='', save=True,
                 save_location=''):
        self.token = token.strip()
        self.ad_account = ad_account.strip()
        self.campaign_id = campaign_id.strip()
        self.adset_id = adset_id.strip()
        self.adgroup_id = adgroup_id.strip()
        self.start = start.strip()
        self.end = end.strip()
        self.save = save
        self.save_location = save_location

    def filtered_call(self):
        # url parameters

        if self.campaign_id != '':
            filter_string = '['
            for campaign_id in self.campaign_id.split(","):
                filter_string += '"' + str(campaign_id) + '",'
            filter_string = filter_string[:-1] + "]"
            filter_campaign_id = ',{"field":"campaign_group.id","operator":"IN","value":' + filter_string + '}'
        else:
            filter_campaign_id = ''

        fields = '&fields=["campaign_name","campaign_group_id","campaign_delivery","results","performance_indicator",' \
                 '"reach","cost_per_result","campaign_budget_value","campaign_budget_type","spend",' \
                 '"campaign_end","campaign_start"]'

        action_breakdown = "&default_summary=true"

        filtering = '&filtering=[{"field":"adgroup.delivery_info","operator":"IN","value":' \
                    '["active","archived","completed","inactive","not_delivering","not_published","pending_review",' \
                    '"recently_completed","recently_rejected","rejected","scheduled","permanently_deleted"]}' \
                    + filter_campaign_id + ']'

        export_columns = '&export_columns=["campaign_name", "campaign_group_id", "campaign_delivery", "results",' \
                         '"performance_indicator", "reach", "cost_per_result", "campaign_budget_value",' \
                         '"campaign_budget_type", "spend", "campaign_end", "campaign_start"]'

        action_list = 0

        non_action_list = ["date_start", "date_stop", "account_id", "spend",
                           "reach"]

        relevance_score = 0
        video_view_list = 0
        action_values = 0

        level = '&level=campaign'

        time_range = '&time_range={"since": "' + self.start + '", "until": "' + self.end + '"}'

        # url
        url = 'https://graph.facebook.com/v2.3/act_' + self.ad_account + '/insights?' \
                                                                         'access_token=' + self.token + \
              '&action_attribution_windows=["default"]' \
              + fields + filtering + action_breakdown + level + time_range + export_columns + '&method=post'
        print url

        # post url
        report_run_id = requests.post(url)
        try:
            report_id = report_run_id.json()['report_run_id']
        except:
            print report_run_id.text

        # get job status
        url = 'https://graph.facebook.com/v2.4/' + report_id + '?access_token=' + self.token
        print "report run url is: ", url
        run = True
        while run is True:
            time.sleep(2)
            response = requests.get(url)
            status = response.json()['async_status']
            print status
            if 'Completed' in status:
                run = False
            elif 'Failed' in status:
                exit()
                break
            else:
                continue

        # get data
        data = JsonParser(report_id, self.token, fields, self.ad_account, action_list, video_view_list,
                          non_action_list, action_values, relevance_score)
        parser = data.parser()

        if self.save:
            with open(str(self.save_location) + 'data_' + str(self.ad_account.strip()) + '.csv',
                      'wb+') as g:
                s = csv.writer(g)
                s.writerow(["Start Date",
                            "End Date",
                            "Account ID",
                            "Spend",
                            "Reach"])
                for row in parser:
                    for data in row:
                        s.writerow(data)
        else:
            return parser
