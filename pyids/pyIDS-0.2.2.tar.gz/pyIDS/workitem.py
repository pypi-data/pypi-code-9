class Workitem:
    def __init__(self, obj):
        self.id = obj["id"]
        self.summary = obj["summary"]
        self.description = obj["description"]
        self.project = obj["projectArea"]["name"]
        self.url = "%s/resource/itemName/%s/%s" % (obj["reportableUrl"].split("/rpt")[0], obj["itemType"], obj["id"])
        self.state = obj["state"]["name"]
        self.type = obj["type"]["name"]
        self.owned_by = obj["owner"]["name"]
        self.created_by = obj["creator"]["name"]
        self.filed_against = obj["category"]["qualifiedName"]
        self.severity = obj["severity"]["name"]
        self.priority = obj["priority"]["name"]
        self.creation_date = obj["creationDate"]
        self.due_date = obj["dueDate"]

        if "comments" in obj:
            if not isinstance(obj["comments"], list):
                self.comments = [{"comment": obj["comments"]["content"],
                                  "creator": obj["comments"]["creator"]["name"],
                                  "creationDate": obj["comments"]["creationDate"]}]
            else:
                self.comments = [{"comment": comment["content"],
                                  "creator": comment["creator"]["name"],
                                  "creationDate": comment["creationDate"]} for comment in obj["comments"]]

        # TODO: Allow a tag to contain a pipe. At the moment it splits them.
        if obj["tags"] is not None:
            self.tags = obj["tags"].split("|")
        else:
            self.tags = None

        if "stringComplexity" in obj:
            self.points = obj["stringComplexity"]
