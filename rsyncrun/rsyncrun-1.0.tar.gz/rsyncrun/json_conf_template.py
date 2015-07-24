# -*-coding:utf-8-*-


class JsonConfTemplate(object):

    name_prefix = "rsyncrun"
    name_prefix_old = "xdeploy"

    example = """{
"sync_projects": {
      "local_to_remote" : {
          "vox-hadoop" : ["/Users/mvj3/17zuoye/hg/vox-hadoop/",     "/home/hadoop/deploy/mvj3.20150414/"],
          "luiti"      : ["/Users/mvj3/github/17zuoye/luiti/",      "/home/hadoop/deploy/share.20150414/"],
          "etl_utils"  : ["/Users/mvj3/github/17zuoye/etl_utils/",  "/home/hadoop/deploy/share.20150414/"],
      },
      "remote_to_remote" : {
          "luiti"      : ["/home/hadoop/deploy/share.20150414/luiti", "/home/hadoop/deploy/share.20150414/"],
          "etl_utils"  : ["/home/hadoop/deploy/share.20150414/etl_utils", "/home/hadoop/deploy/share.20150414/"],
      },
      "projects_lazy_install_by_python": [
           "etl_utils",
           "etl_common",
           "table_dump",
           "table_tmp",
           "old_student_teacher_report"
      ],
      "exclude_rules": [
          "*.pyc",
          "build",
          "dist",
          "*.egg-info"
      ]
    },
    "remote_server": {
        "user"        : "hadoop",
        "host"        : "8.8.8.8",
        "execute_dir" : "/home/hadoop/deploy/mvj3.20150414/",
    },
    "scripts_before_run": [
    ],
    "launch": {
        "template": "cd %s; luiti run --task-name %s --date-value %sT00:00:00+08:00",
        "params_list": [
            ["old_student_teacher_report", "Redmine7518EnglishStudentReportWeek", "2015-03-09"],
            ["table_dump", "DumpSchoolCityRefFromDatabaseDay", "2015-03-09"]
        ],
        "params_index": 0
    }
}
"""
