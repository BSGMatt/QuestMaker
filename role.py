# 
#   This is the constructor for a role class:
#   name -> name of the role
#   hunt -> the higher the value, the more likely hunts
#   will be successful. 
#   endurance -> the higher the value, the more likely you will survive
#   encounters without taking damage. 
#   bargaining -> the higher the value, the more likely you will get your
#   way when bargaining. 
#
class Role:
    def __init__(self, name: str, hunt: int, endurance: int, bargaining: int):
        self.name = name;
        self.hunt = hunt;
        self.endurance = endurance;
        self.bargaining = bargaining;

#Below are the defined roles. 
ROLE_HUNTER = Role("Hunter", 75, 50, 25);
ROLE_DOCTOR = Role("Doctor", 25, 75, 50);
ROLE_MERCHANT = Role("Merchant", 50, 25, 75);
ROLE_CIVILIAN = Role("Civilian", 50, 50, 50);