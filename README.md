# Hack-The-North-2023


### Integration Signals and Data Transfers
- First Left Blink -> QRDETECT Signal. Search for QR Code and scrape website for user data.
    - Store the name and information in a database (?)
    - Returns all of the data in a variable called name_and_data, with the name and data separated by a newline
- Second Left Blink -> FACEDETECT Signal. Add face to database. 
    - POST api.efetascioglu.com/api/add_face.  data: {"face": base64 encoded image, "eye_pos": (x, y), "name_and_data": name and data (separated by a newline)}
    - Returns: {"success": true/false}
- Right Blink -> RECALL Signal. Search for face in database
    - POST api.efetascioglu.com/api/search_face.  data: {"face": base64 encoded image, "eye_pos": (x, y)}
    - Returns: {"success": true/false, "name_and_data": name and data (separated by a newline)}