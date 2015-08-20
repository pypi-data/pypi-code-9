contact_schema = {
    "type":"object",
    "properties":{
        "email_addresses":{
            "type":"array",
            "additionalItems":False,
            "required":True,
            "description":"Array of email address of the contact.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "maxItems":1,
            "minItems":1,
            "items":{
                "additionalProperties":False,
                "type":"object",
                "properties":{
                    "id":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"Email Address ID",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "status":{
                        "type":["string", "null"],
                        "enum":["ACTIVE", "UNCONFIRMED", "OPTOUT", "REMOVED", "NON_SUBSCRIBER"],
                        "readonly":True,
                        "description":"Email address status, valid values: <ul><li>ACTIVE: Contact is an active member of a contactlist<li>UNCONFIRMED: Contact has not confirmed their email address<li>OPTOUT: Contact has unsubscribed from the account owner's contactlist is on the Do Not Mail list; they cannot be manually added to any contactlist<li>REMOVED: Contact has been taken off all contactlists, and can be added to a contactlist<li>NON_SUBSCRIBER: someone who is not a contact, but has registered for an event the account owner has created, <li>VISITOR: a person who has \"liked\" an account owners social campaign page</ul>",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "confirm_status":{
                        "type":["string", "null"],
                        "enum":["CONFIRMED", "NO_CONFIRMATION_REQUIRED", "UNCONFIRMED"],
                        "readonly":True,
                        "description":"Confirmed status of the email address, valid values: <ul><li>CONFIRMED: contact has confirmed their email address; confirmed contacts are not editable<li>NO_CONFIRMATION_REQUIRED: Contact has been added by the account owner with prior permission<li>UNCONFIRMED: Contact has not yet confirmed their email address with Constant Contact</ul>",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "opt_in_source":{
                        "type":["string", "null"],
                        "enum":["ACTION_BY_VISITOR", "ACTION_BY_OWNER"],
                        "description":"How the contact was added to list, valid values: <ul><li>ACTION_BY_VISITOR means the contact added themself<li>ACTION_BY_OWNER - the list owner added the contact</ul> This value is set automatically when the contact is created, and cannot be edited. It's value must match the <span class=\"highlightText\"><code>action_by value</code></span>; if not set on POST, takes on value of <span class=\"highlightText\"><code>action_by property</code></span>",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "opt_out_source":{
                        "type":["string", "null"],
                        "enum":["ACTION_BY_VISITOR", "ACTION_BY_OWNER"],
                        "description":"If the contact has a status of OPTOUT, this field describes who initiated the action: <ul><li>ACTION_BY_VISITOR - contact initiated the OPTOUT<li>ACTION_BY_OWNER - the list owner initiated the OPTOUT</ul>",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "opt_in_date":{
                        "type":["string", "null"],
                        "format":"date-time",
                        "description":"date contact Opted-in",
                        "readonly":True,
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "opt_out_date":{
                        "type":["string", "null"],
                        "format":"date-time",
                        "readonly":True,
                        "description":"If the contact has a status of OPTOUT, this field displays the date the OPTOUT occurred",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "email_address":{
                        "type":"string",
                        "antiSamyLevel":2,
                        "format":"email",
                        "maxLength":80,
                        "minLength":6,
                        "required":True,
                        "description":"Contact's email address, cannot exceed 80 characters",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    }
                }
            }
        },
        "prefix_name":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":4,
            "description":"Salutation (Mr., Ms., Sir, Mrs., Dr., etc)",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "first_name":{
            "antiSamyLevel":2,
            "type":["string", "null"],
            "maxLength":50,
            "description":"Contact's first name",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True

        },
        "middle_name":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"Contact's middle name",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "last_name":{
            "type":["string", "null"],
            "maxLength":50,
            "description":"Contact's last name",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "job_title":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"Contact's job title",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "company_name":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"Contact's company",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "home_phone":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "format":"phone",
            "maxLength":50,
            "description":"Contact's home phone number",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "work_phone":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "format":"phone",
            "maxLength":50,
            "description":"Contact's Work phone number",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "cell_phone":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "format":"phone",
            "maxLength":50,
            "description":"Contact's cell phone number",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True

        },
        "fax":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "format":"phone",
            "maxLength":50,
            "description":"Contact's fax number",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "addresses":{
            "type":["array", "null"],
            "additionalItems":False,
            "description":"Addresses of the contact.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "maxItems":2,
            "items":{
                "type":["object"],
                "additionalProperties":False,
                "properties":{
                    "id":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"Address ID",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "address_type":{
                        "type":["string", "null"],
                        "enum":["PERSONAL", "BUSINESS"],
                        "description":"Mailing address type, valid values are PERSONAL, BUSINESS",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "line1":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":50,
                        "description":"Street Address line 1",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "line2":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":50,
                        "description":"Street Address line 2",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "line3":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":50,
                        "description":"Street Address line 3",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "city":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":50,
                        "description":"Contact's city",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "state_code":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":2,
                        "description":"Standard 2 letter (capitalized) abbreviation for contact's state; field is case sensitive",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "state":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":50,
                        "description":"The state name. If state_code is a valid US State, this will be the name of the state. Otherwise, this can be populated by the user.",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "country_code":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":2,
                        "description":"Standard ISO 3166-1 alpha-2 2-letter (capitalized) country code for the contact; field is case sensitive",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "postal_code":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":25,
                        "description":"Postal ZIP code for the contact",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "sub_postal_code":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":25,
                        "description":"Zip Code 'plus 4' for the contact",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    }
                }
            }
        },
        "notes":{
            "type":["array", "null"],
            "description":"Notes associated with the contact.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "additionalItems":False,
            "maxItems":1,
            "items":{
                "type":["object"],
                "additionalProperties":False,
                "properties":{
                    "id":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"Note ID.",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "note":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":500,
                        "minLength":1,
                        "description":"Note.",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "created_date":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "format":"date-time",
                        "description":"Date that the note was created, in ISO 8601 format",
                        "readonly":True,
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "modified_date":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "format":"date-time",
                        "description":"Date that the note was modified, in ISO 8601 format",
                        "readonly":True,
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    }
                }
            }
        },
        "custom_fields":{
            "type":["array", "null"],
            "additionalItems":False,
            "description":"Custom fields.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "items":{
                "additionalProperties":False,
                "type":["object"],
                "properties":{
                    "name":{
                        "type":"string",
                        "pattern":"^[Cc]ustom_?[Ff]ield_?([1-9]|1[0-5])$",
                        "description":"You must name each custom field name custom_field_X, or CustomFieldX, or Custom_FieldX, where X is a number 1-15. Only custom fields with values are shown in response to a GET call.",
                        "required":True,
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "label":{
                        "type":["string", "null"],
                        "pattern":"^CustomField([1-9]|1[0-5])$",
                        "description":"You must name each custom field label CustomField1, CustomField2,...CustomField15. Only custom fields with values are shown in response to a GET call.",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "value":{
                        "type":"string",
                        "maxLength":50,
                        "description":"Custom field value.",
                        "required":True,
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True,
                        "antiSamyLevel":3
                    }
                }
            }
        },
        "confirmed":{
            "type":["boolean", "null"],
            "description":"If the contact has confirmed their email subscription, this value is True, and it is False if they have not.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "created_date":{
            "type":["string", "null"],
            "format":"date-time",
            "readonly":True,
            "description":"Date and Time of creation of the contact in ISO-8601",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "modified_date":{
            "type":["string", "null"],
            "format":"date-time",
            "readonly":True,
            "description":"Date & time contact's information was last updated, in ISO 8601 format; value is the same as <span class=\"highlightText\"><code>insert_date</span></code> if contact has not been updated.",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "lists":{
            "type":["array", "null"],
            "additionalProperties":False,
            "description":"Contactlists that the contact is a member of",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "additionalItems":False,
            "items":{
                "type":["object"],
                "properties":{
                    "id":{
                        "type":"string",
                        "antiSamyLevel":2,
                        "required":True,
                        "readonly":True,
                        "description":"Unique ID of contactlist the contact is a member of",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    },
                    "name":{
                        "type":["string", "null"],
                        "antiSamyLevel":2,
                        "maxLength":255,
                        "description":"Name of the contact list",
                        "readonly":True,
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "created_date": {
                        "type": ["string", "null"],
                        "antiSamyLevel":2,
                        "description": "date contact list created",
                        "readonly": True,
                        "displayInPOST": False,
                        "displayInPUT": False,
                        "displayInGET": False
                    },
                    "modified_date": {
                        "type": ["string", "null"],
                        "description": "date contact list modified",
                        "readonly": True,
                        "displayInPOST": False,
                        "displayInPUT": False,
                        "displayInGET": False
                    },
                    "contact_count":{
                        "type":["integer", "null"],
                        "minimum":0,
                        "readonly":True,
                        "description":"Number of contacts in the list",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "status":{
                        "type":["string", "null"],
                        "enum":["ACTIVE", "HIDDEN", "REMOVED"],
                        "readonly":True,
                        "description":"Contact list status, valid values: <ul><li>ACTIVE: List is the current default contactlist</li><li>HIDDEN - List is not the default contact list</li></ul>",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    }
                }
            }
        },
        "source":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"Describes how the contact was added, from an application, web page, etc.",
            "readonly":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "source_details":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":255,
            "description":"How contact was created, value is API key if created using API",
            "readonly":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "id":{
            "type":["string", "null"],
            "readonly":True,
            "description":"Unique ID for the contact",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "status":{
            "type":["string", "null"],
            "enum":["ACTIVE", "UNCONFIRMED", "OPTOUT", "REMOVED", "NON_SUBSCRIBER"],
            "readonly":True,
            "description":"Contact status, valid values are: <ul><li>ACTIVE: Contact is an active member of a contactlist</li><li>UNCONFIRMED: Contact has not confirmed their email address</li><li>OPTOUT: Contact has unsubscribed from the account owner's contactlist is on the Do Not Mail list; they cannot be manually added to any contactlist</li><li>REMOVED: Contact has been taken off all contactlists, and can be added to a contactlist</li><li>NON_SUBSCRIBER: someone who is not a contact, but has registered for an event the account owner has created,</li> <li>VISITOR: a person who has \"liked\" an account owners social campaign page</li></ul>",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        }
    },
    "additionalProperties":False
}
