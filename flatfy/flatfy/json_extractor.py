

def extract_field(json_data, value):

    result = next((json_obj for json_obj in json_data["geo_entities"] if json_obj["type"] == value), None)

    if result:
        return result['name']
    else:
        return "N/A"
