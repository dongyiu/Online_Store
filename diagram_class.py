import os
import shutil
import webbrowser
import plantuml

uml_text = """
@startuml
class User {
    -sessionId: string
    +purchase(Item)
}

class Admin {
    -userId: string
    -password: string
    +login()
    +add_item(Item)
    +delete_item(Item)
}

class Item {
    -id: string
    -name: string
    -image: string
    -price: Number
    +generate_id()
    +add_item_to_db()
    +remove_item_from_db()
}


class OnlineStore {
    -items: Item[]
    +get_items()
    +add_item(Item)
    +remove_item(Item)
}

class AuctionHouse {
    -items: Item[]
    +get_items()
}

User <-- Admin
AuctionHouse <-- User
OnlineStore <-- User
AuctionHouse <-- Item
OnlineStore <-- Item

@enduml
"""

img_path = 'UML_Diagrams/class_diagram.png'

# Create the UML_Diagrams directory if it doesn't exist
os.makedirs('UML_Diagrams', exist_ok=True)

# Delete the file if it already exists
if os.path.exists(img_path):
    os.remove(img_path)

# Generate the image and save it to a file
img_bytes = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/').processes(uml_text)
with open(img_path, 'wb') as f:
    f.write(img_bytes)

# Print the file path and open the image in the default viewer
print(f"Generated class diagram at {os.path.abspath(img_path)}")
webbrowser.open(os.path.abspath(img_path))

# python3 diagram_class.py