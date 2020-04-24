class User:

    counter = 1

    def __init__(self, name, password):

        # Keep track of id number.
        self.id = User.counter
        User.counter += 1

        # Details about user.
        self.name = name
        self.password = password
 

class Review:

    counter = 1

    def __init__(self, ID, username, asin, mark, text):
      
        # Keep track of id number.
        self.ID = ID
        #Details about review.
        self.username=username
        self.asin=asin
        self.mark=mark
        self.text=text