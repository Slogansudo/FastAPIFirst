from db.database import ENGINE, Base
from db.models import Users, Address, Places, TravelCategory, Travels, Comments


Base.metadata.create_all(bind=ENGINE)
