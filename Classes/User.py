class User:
#initialise user
    def __init__(self, userid, firstName, lastName, userEmail, userPassword, isAdmin=False, cart=None):

        self.id = userid
        self.first_name = firstName
        self.lastName = lastName
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.isAdmin = isAdmin
        self.cart = cart if cart is not None else []

