from 

if __name__ == "__main__":
    # Example usage:
    recognizer = SimpleFaceRecognizer()
    # Set up the database in RAM
    recognizer.add_face(get_absolute_path("images/efe_1.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_2.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/efe_3.jpg"), "Efe Tascioglu")
    recognizer.add_face(get_absolute_path("images/tyler_1.jpg"), "Tyler Tian")
    app.run(host='0.0.0.0')