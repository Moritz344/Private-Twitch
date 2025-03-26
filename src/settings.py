import json

def get_data() -> str:

    with open("data.json","r") as file:

        data = json.load(file)
        
        colorscheme = data["settings"]["colorscheme"]
        borderSpacing = data["settings"]["borderSpacing"]
        font_size = data["settings"]["font_size"]
        
        # COLORSCHEMES (TEXT)

        coffeine = data["colorschemes"]["coffeine"]
        lavender = data["colorschemes"]["lavender"]
        quiet = data["colorschemes"]["quiet"]


        return borderSpacing,coffeine,lavender,quiet,font_size,colorscheme

borderSpacing,coffeine,lavender,quiet,font_size,colorscheme = get_data()
