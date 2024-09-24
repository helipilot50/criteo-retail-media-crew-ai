import yaml
import os
import json




def test_embedded_json():

    # Get the directory of the current file
    current_file_directory = os.path.dirname(os.path.abspath(__file__))

    embedded = current_file_directory +"/with_embedded_json.yaml"
    assert os.path.exists(embedded)
    # Open and read the YAML file
    with open(embedded, 'r') as file:
        data = yaml.safe_load(file)

    # Print the parsed data
    print(json.dumps(data, indent=4))
    assert data["create_campaign"] is not None
    assert data["create_campaign"]["description"] is not None
    