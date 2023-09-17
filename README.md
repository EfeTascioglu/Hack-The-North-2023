# Hack-The-North-2023


### Integration Signals and Data Transfers
- First Left Blink -> Search for QR Code and scrape website (?)
    - Store the name and information in a database (?)
    - Returns all of the data in a variable called name_and_data, with the name and data separated by a newline
- Second Left Blink -> Add face to database
    - POST api.efetascioglu.com/api/add_face.  data: {"face": base64 encoded image, "eye_pos": (x, y), "name and data": name and data (separated by a newline)}
    - Returns: {"success": true/false}
- Right Blink -> Search for face in database
    - POST api.efetascioglu.com/api/search_face.  data: {"face": base64 encoded image, "eye_pos": (x, y)}
    - Returns: {"success": true/false, "name and data": name and data (separated by a newline)}