from migrate_property_data import migrate_property_data
from migrate_school_data import migrate_schools
from migrate_suburb_profile import migrate_suburb_profile    

if __name__ == "__main__":
    migrate_property_data()
    migrate_schools()
    migrate_suburb_profile()
