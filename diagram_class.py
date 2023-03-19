import os
import shutil
import webbrowser
import plantuml

uml_text = """
@startuml
class User {
    -id: int
    -name: str
    -email: str
    -password: str
    +login()
    +logout()
    +search_item()
    +view_results()
    +select_item()
    +add_to_cart()
    +checkout()
}

class Admin {
    -id: int
    -name: str
    -email: str
    -password: str
    +login()
    +logout()
    +add_item()
    +delete_item()
}

class Item {
    -id: int
    -name: str
    -category: str
    -price: float
    -is_sold: bool
    +generate_id()
    +add_item_to_db()
    +remove_item_from_db()
}

class Cart {
    -items: list
    -total_price: float
    +add_item()
    +remove_item()
    +checkout()
}

class OnlineStore {
    -users: dict
    -admins: dict
    -items: dict
    -cart: Cart
    +add_user()
    +remove_user()
    +add_admin()
    +remove_admin()
    +get_item()
    +add_item()
    +remove_item()
    +display_live_updates()
}

class AuctionHouse {
    -items: dict
    +get_item()
    +add_item()
    +remove_item()
    +display_live_updates()
}

User --> Item: selects
User --> Cart: adds
User --> Cart: removes
User --> OnlineStore: checks out
User --> OnlineStore: views
User --> OnlineStore: searches
User --> OnlineStore: logs in
User --> OnlineStore: logs out
Admin --> Item: adds
Admin --> Item: removes
Admin --> OnlineStore: logs in
Admin --> OnlineStore: logs out
OnlineStore --> User
OnlineStore --> Admin
OnlineStore --> Item
OnlineStore --> Cart
OnlineStore --> AuctionHouse
AuctionHouse --> Item
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