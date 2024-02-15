from crawl_realestate import crawl_realestate
from crawl_school import crawl_school
from crawl_suburb_profile import crawl_suburb_profile

from migrate_property_data import migrate_property_data
from migrate_school_data import migrate_schools
from migrate_suburb_profile import migrate_suburb_profile    

if __name__ == "__main__":
    """
    This script is used to crawl for data and migrate it to the database.
    crawl_realestate() and migrate_property_data() are reserved for run 2 development
    """

    # crawl_realestate()
    crawl_school()
    crawl_suburb_profile()

    # migrate_property_data() 
    migrate_schools()
    migrate_suburb_profile()

