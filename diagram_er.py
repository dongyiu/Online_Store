import os
import shutil
import webbrowser
import plantuml

uml_text = """
@startuml
entity Item {
  * item_id: String   PK
  * image: String
  * price: Number
  * name: String

}

entity User {
  * session_id: String   PK
}

entity Admin {
  * user_id: String   PK
  * password: String

}

Item ||..|| User
Item ||..|| Admin

@enduml
"""

img_path = 'UML_Diagrams/er_diagram.png'

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