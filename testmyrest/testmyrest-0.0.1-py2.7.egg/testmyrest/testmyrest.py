import json
import jsonschema
import os

def validate_schema_data(schema_path, data):
    schema = open(schema_path).read()
    jsonschema.validate(json.loads(data), json.loads(schema))

def generate_json_schemas(schema_file_path):                            #Generates single Json schema files from a RAML schema collection 
    with open(schema_file_path, "r") as f_in:                           #and puts them in a subfolder schemas/ 
        lines = (line.rstrip() for line in f_in)        
        lines = (line for line in lines if line)
        output_file_name = ""
        output = None
        if not os.path.exists("schemas"):
            os.makedirs("schemas")
        for l in lines:
            if "|" in l:
                if output_file_name != "":
                    output.close()
                output_file_name , trash = l.split(":")
                output = open("schemas/" + lower_first_helper(output_file_name) + ".schema", "w")
            else:
                output.write(l + "\n")
        output.close()

def list_of_resourcetypes(schema_file_path):
    schema_list = []
    with open(schema_file_path, "r") as schemas:
        lines = (line.rstrip() for line in schemas)
        for l in lines:
            if "|" in l:
                temp_schema_name , trash = l.split(":")
                schema_list.append(temp_schema_name)
    return schema_list

def list_of_adresses_and_schemas(file_path, schema_file_path):
    output_list = []
    adress_list = []
    with open(file_path, "r") as raml:
        lines = (line.rstrip() for line in raml)
        lines = (line for line in lines if line)
        for l in lines:
            if l[0] == "/":
                trash, temp = l.split("/")
                temp2, trash = temp.split(":")
                adress_list.append(temp2.lower())                       #Adresses in lowercase
    schema_iterator = os.walk("schemas/")
    schema_list = schema_iterator.next()[2]
    for schema in schema_list:
        temp, trash = schema.split(".")
        if temp.lower() in adress_list:
            output_list.append( (temp.lower(), "schemas/" + schema) )
    return output_list

def lower_first_helper(name):                                           #Helper for turning CamelCase into camelCase
    if len(name) == 0:                                                  #strings with more than one uppercase char prefix will not be changed
        return name
    else:
        if name[1].isupper():                                           #Apple iSupper(): The fastest, most powerful iMeal() yet.
            return name
        else:
            return name[0].lower() + name[1:]                           
 