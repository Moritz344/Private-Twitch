import json
def get_data() -> str:

    with open("data.json","r") as file:

        data = json.load(file)
        

        text_color = data["settings"]["text_color"]


        return text_color

text_color = get_data()
