campaign_schema = {
    "description":"An Email Campaign",
    "type":"object",
    "properties":{
        "id":{
            "type":["string", "null"],
            "readonly":True,
            "description":"The unique identifier for the Campaign",
            "displayInPOST":False,
            "displayInPUT":True,
            "displayInGET":True
        },
        "name":{
            "type":"string",
            "antiSamyLevel":2,
            "required":True,
            "minLength":1,
            "maxLength":80,
            "description":"Name of the email campaign; each email campaign name must be unique within a user's account",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "subject":{
            "type":"string",
            "antiSamyLevel":2,
            "minLength":1,
            "required":True,
            "maxLength":200,
            "description":"The Subject Line for the email campaign",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "from_name":{
            "type":"string",
            "antiSamyLevel":2,
            "maxLength":100,
            "required":True,
            "minLength":1,
            "description":"Name displayed in the From field to indicate whom the email is from",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "from_email":{
            "type":"string",
            "antiSamyLevel":2,
            "maxLength":80,
            "minLength":6,
            "format":"email",
            "description":"The email address the email campaign originated from, this must be a <a href=\"/docs/account/verify-email-addresses.html\">verified email address</a> for the account owner",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "reply_to_email":{
            "type":"string",
            "antiSamyLevel":2,
            "maxLength":80,
            "minLength":6,
            "format":"email",
            "description":"The reply-to email address for the email campaign, this must be a <a href=\"/docs/account/verify-email-addresses.html\">verified email address</a> for the account owner",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "template_type":{
            "type":["string", "null"],
            "enum":["STOCK", "CUSTOM", "TEMPLATE_V2"],
            "description":"The template used to create the email campaign; valid values are STOCK, CUSTOM and TEMPLATE_V2",
            "readonly":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "status":{
            "type":["string", "null"],
            "enum":["DRAFT", "RUNNING", "SCHEDULED", "SENT", "ARCHIVE_PENDING", "ARCHIVED", "CLOSE_PENDING", "CLOSED", "HISTORY", "OPEN"],
            "description":"Current status of the email campaign, valid values: <ul><li>DRAFT: This is the default status for an email that is still being worked on. Draft emails have been saved and can be edited at any time.<li>RUNNING: The email messagSente is in the process of being sent and can't be edited.<li>SENT: An email that has been sent has already been mailed to it's contact list. It can't be edited.<li>SCHEDULED: A scheduled email has been set to mail on a specific date and cannot be edited unless it's returned to Draft status.</ul>",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "is_permission_reminder_enabled":{
            "type":["boolean", "null"],
            "description":"If True, displays <span class=\"highlightText\"><code>permission_reminder_text</code></span> at top of email message reminding the recipient they are recieving the email because they have subscribed to an email list.",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "permission_reminder_text":{
            "type":["string", "null"],
            "maxLength":1500,
            "description":"REQUIRED if <span class=\"highlightText\"><code>is_permission_reminder_enabled</code></span> = True; enter text to display in the permission reminder message; otherwise not required",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "antiSamyLevel":3
        },
        "is_view_as_webpage_enabled":{
            "type":["boolean", "null"],
            "description":"If True, displays the text and link specified in <span class=\"highlightText\"><code>permission_reminder_text</code></span> to view web page version of email message",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "view_as_web_page_text":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"REQUIRED if <span class=\"highlightText\"><code>is_view_as_webpage_enabled</code></span> = True; enter text to display with link at the top of email message, such as \"View this message as a web page\"; otherwise not required",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "view_as_web_page_link_text":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"REQUIRED if <span class=\"highlightText\"><code>is_view_as_webpage_enabled</code></span> = True; enter desired link text to display in the View As Web page link; otherwise not required",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "greeting_salutations":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":50,
            "description":"The salutation used in the email message(e.g. Dear)",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "greeting_name":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "enum":["FIRST_NAME", "LAST_NAME", "FIRST_AND_LAST_NAME", "NONE"],
            "description":"Specifies the personalized content for each contact that will be used in the greeting, valid values are: <ul><li>FIRST_NAME - contacts first name on record<li>LAST_NAME - contacts last name of record<li>FIRST_AND_LAST_NAME - use both the contacts first and last name<li>NONE; if NONE then the email message will use the <span class=\"highlightText\"><code>greeting_string</code></span> parameter.</ul>",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "greeting_string":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "maxLength":1500,
            "description":"Specifies the greeting text used if not using <span class=\"highlightText\"><code>greeting_name</code></span> and <span class=\"highlightText\"><code>greeting_salutations</code></span>, which have precedence over <span class=\"highlightText\"><code>greeting_string</code></span>)",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "email_content":{
            "type":["string", "null"],
            "pattern":"[\\S\\s]*<[hH][tT][mM][lL][^>]*>[\\S|\\s]*<[bB][oO][dD][yY][^>]*>[\\S|\\s]*</[bB][oO][dD][yY]>[\\S|\\s]*</[hH][tT][mM][lL]>[\\S\\s]*$",
            "maxLength":930000,
            "description":"The full HTML/XHTML email campaign message content",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "antiSamyLevel":-1
        },
        "email_content_format":{
            "type":["string", "null"],
            "enum":["HTML", "XHTML"],
            "description":"Specifies the email campaign message format, valid values: HTML, XHTML",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "text_content":{
            "type":["string", "null"],
            "maxLength":930000,
            "description":"The content for the text-only version of the email campaign. Viewed by recipients whose email client does not accept HTML email.",
            "minLength":1,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "antiSamyLevel":-1
        },
        "style_sheet":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "description":"Valid only if <span class=\"highlightText\"><code>email_content_format</code></span> = XHTML; see the <a href=\"http://www.constantcontact.com/learning-center/guides/details/building-your-email-with-the-advanced-editor-tool.jsp\">Advanced Editor Users Guide</a> for specific formatting constraints. Lists the stylesheet elements used to format the email campaign message",
            "readonly":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True
        },
        "created_date":{
            "type":["string","null"],
            "format":"date-time",
            "minLength":1,
            "description":"Date the email campaign was last sent to contacts, in ISO-8601 format",
            "readonly":True,
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "last_sent_date":{
            "type":["string","null"],
            "format":"date-time",
            "minLength":1,
            "readonly":True,
            "description":"Date the email campaign was last sent to contacts, in ISO-8601 format",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "permalink_url":{
            "type":["string", "null"],
            "antiSamyLevel":2,
            "readonly":True,
            "description":"System generated, non-expiring link to use for sharing a sent email campaign using social channels. Only available for email campaigns with status of SENT. If the user removes the email campaign from their campaign list, the link is taken down. Any shared links will return a 404. ",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "modified_date":{
            "type":["string","null"],
            "format":"date-time",
            "minLength":1,
            "readonly":True,
            "description":"Date the email campaign was last modified, in ISO-8601 format",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "last_run_date":{
            "type":["string","null"],
            "format":"date-time",
            "minLength":1,
            "readonly":True,
            "description":"Date the email campaign was last run, in ISO-8601 format",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },
        "next_run_date":{
            "type":["string","null"],
            "format":"date-time",
            "minLength":1,
            "readonly":True,
            "description":"Date the email campaign is next scheduled to run and be sent to contacts, in ISO-8601 format",
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True
        },

        "tracking_summary":{
            "type":["object","null"],
            "description":"Tracking summary information for this particular campaign.",
            "readonly":True,
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "properties":{
                "bounces":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of email address bounces for this campaign",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "clicks":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of recipients who clicked a link in this email campaign",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "forwards":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of recipients who forwarded this email campaign",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "opens":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of recipients who opened this  email campaign",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "sends":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of recipients this email campaign was sent to",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "unsubscribes":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of recipients who unsubscribed from this campaign",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                },
                "spam_count":{
                    "type":["integer","null"],
                    "readonly":True,
                    "description":"Number of spam reports",
                    "displayInPOST":False,
                    "displayInPUT":False,
                    "displayInGET":True
                }
            },
            "additionalProperties":False
        },

        "message_footer":{
            "type":"object",
            "description":"Contains the content of the email campaign message footer; minimum required fields are city, address_line1,country, postal code",
            "displayInPOST":True,
            "displayInPUT":True,
            "displayInGET":True,
            "properties":{
                "city":{
                    "type":"string",
                    "antiSamyLevel":2,
                    "minLength":1,
                    "required":True,
                    "description":"City where the organization sending the email campaign located",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "state":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "description":"If in the United States, 2 letter (capitalized) code of the state that the organization sending the email campaign is located, field is case sensitive",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "country":{
                    "type":"string",
                    "enum":["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH",
                        "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF", "BI",
                        "KH", "CM", "CA", "CV", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
                        "HR", "CY", "CZ", "DK", "DJ", "DM", "DO", "TL", "EC", "EG", "SV", "U1", "GQ", "ER", "EE", "ET", "FO", "FK",
                        "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT",
                        "GG", "GN", "GW", "GY", "HT", "HM", "HN", "HK", "HU", "IS", "IN", "ID", "IQ", "IE", "IM", "IL", "IT", "JM",
                        "JP", "JE", "JO", "KZ", "KE", "KI", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO",
                        "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME",
                        "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "AN", "NT", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "U4",
                        "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RE", "RO",
                        "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "U3", "SN", "RS", "SC", "SL",
                        "SG", "SK", "SI", "SB", "SO", "ZA", "GS", "KR", "ES", "LK", "SR", "SJ", "SZ", "SE", "CH", "TW", "TJ", "TZ",
                        "TH", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE", "GB", "US", "USA", "UM", "UY",
                        "UZ", "VU", "VA", "VE", "VN", "VG", "VI", "U2", "WF", "EH", "YE", "ZM", "ZW"],
                    "required":True,
                    "description":"2 letter (capitalized) ISO 3166-1 code of the country that the organization sending the email campaign is located, field is case-sensitive",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "organization_name":{
                    "type":"string",
                    "antiSamyLevel":2,
                    "maxLength":255,
                    "minLength":1,
                    "description":"Name of the organization sending the email campaign",
                    "required":True,
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "address_line_1":{
                    "type":"string",
                    "antiSamyLevel":2,
                    "maxLength":50,
                    "description":"Line 1 - originating organization's street address",
                    "required":True,
                    "minLength":1,
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "address_line_2":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "maxLength":50,
                    "description":"Line 2 - originating organization's street address",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "address_line_3":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "maxLength":50,
                    "description":"Line 3 - originating organization's street address",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "international_state":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "maxLength":50,
                    "description":"If not from US, the international state of the originating organization",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "postal_code":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "maxLength":25,
                    "description":"Address Postal (ZIP) code of the originating organization",
                    "minLength":1,
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "include_forward_email":{
                    "type":["boolean", "null"],
                    "antiSamyLevel":2,
                    "description":"Specifies if the email message footer includes a link for forwarding the email message",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "forward_email_link_text":{
                    "type":["string", "null"],
                    "antiSamyLevel":2,
                    "maxLength":45,
                    "description":"REQUIRED if <span class=\"highlightText\"><code>include_forward_email = True</code></span>, contains the text of the forward email link, otherwise not required",
                    "displayInPOST":True,
                    "displayInGET":True
                },
                "include_subscribe_link":{
                    "type":["boolean", "null"],
                    "description":"Specifies if the footer includes a subscribe link",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                },
                "subscribe_link_text":{
                    "type":["string", "null"],
                    "maxLength":45,
                    "description":"REQUIRED if <span class=\"highlightText\"><code>include_subscribe_link = True</code></span>, contains the text of the <span class=\"highlightText\"><code>subscribe_link</code></span>, otherwise not required",
                    "displayInPOST":True,
                    "displayInPUT":True,
                    "displayInGET":True
                }
            },
            "additionalProperties":False
        },
        "click_through_details":{
            "type":["array", "null"],
            "description":"Tracking summary information for this particular campaign.",
            "readonly":True,
            "displayInPOST":False,
            "displayInPUT":False,
            "displayInGET":True,
            "items":{
                "type":["object", "null"],
                "properties":{
                    "url":{
                        "type":["string","null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"URL of the link in campaign.",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "url_uid":{
                        "type":["string","null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"ID of the URL",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    },
                    "click_count":{
                        "type":["integer","null"],
                        "antiSamyLevel":2,
                        "readonly":True,
                        "description":"Click count on this link.",
                        "displayInPOST":False,
                        "displayInPUT":False,
                        "displayInGET":True
                    }
                }
            },
            "additionalProperties":False,
            "additionalItems":False
        },

        "sent_to_contact_lists":{
            "type":["array", "null"],
            "additionalProperties":False,
            "additionalItems":False,
            "description":"Collection of contact lists ids that are associated with this campaign",
            "items":{
                "type":["object"],
                "properties":{
                    "id":{
                        "type":"string",
                        "antiSamyLevel":2,
                        "required":True,
                        "description":"The unique identifier for this contact list.",
                        "displayInPOST":True,
                        "displayInPUT":True,
                        "displayInGET":True
                    }
                }
            }
        }
    },
    "additionalProperties":False
}
