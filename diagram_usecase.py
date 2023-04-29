import os
import shutil
import webbrowser
import plantuml

uml_text = """
@startuml
title Online Store Use Case Diagram

actor User
actor Admin

rectangle "Online Store" {
    User --> (Purchase Item)

    Admin --> (Delete Item)
    Admin --> (Add Item)

    (Add Item) ..> (Authenticate User) : extend
    (Add Item) <.. (Generate Unique Identifier) : includes
    (Add Item) <.. (Create Item) : includes

    (Delete Item) ..> (Authenticate User) : extend
    (Delete Item) <.. (Search Item) : includes
    (Search Item) <.. (Remove Item From Database) : includes

    (Purchase Item) <.. (Search Item) : includes

}
@enduml
"""

img_path = 'UML_Diagrams/use_case_diagram.png'

# Create the UML_Diagrams directory if it doesn't exist
os.makedirs('UML_Diagrams', exist_ok=True)

# Delete the file if it already exists
if os.path.exists(img_path):
    os.remove(img_path)

try:
    # Generate the image and save it to a file
    img_bytes = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/').processes(uml_text)
    with open(img_path, 'wb') as f:
        f.write(img_bytes)
        
    # Print the file path and open the image in the default viewer
    print(f"Generated use case diagram at {os.path.abspath(img_path)}")
    webbrowser.open(os.path.abspath(img_path))
    
except plantuml.PlantUMLHTTPError as e:
    print(f"Failed to generate use case diagram: {e}")

# python3 diagram_usecase.py