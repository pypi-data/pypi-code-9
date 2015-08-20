contact_list_schema = {
    "type":"object",
    "properties":{
        "id":{
            "type":["string", "null"],
            "readonly":True,
            "required":False,
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "name": {
            "type": "string",
            "antiSamyLevel":2,
            "maxLength": 255,
            "required": True,
            "minLength": 1,
            "displayInPOST": True,
            "displayInPUT": True,
            "displayInGET": True
        },
        "created_date": {
            "type": ["string", "null"],
            "description": "date contact list created",
            "readonly": True,
            "displayInPOST": False,
            "displayInPUT": False,
            "displayInGET": True
        },
        "modified_date": {
            "type": ["string", "null"],
            "description": "date contact list modified",
            "readonly": True,
            "displayInPOST": False,
            "displayInPUT": False,
            "displayInGET": True
        },
        "contact_count":{
            "type":["integer", "null"],
            "minimum":0,
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "status":{
            "type":"string",
            "enum":["ACTIVE", "HIDDEN"],
            "required":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        }
    },
    "additionalProperties":False
}