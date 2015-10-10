from parse_rest.installation import Push
from parse_rest.connection import register

from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY

register(APPLICATION_ID, REST_API_KEY)
Push.message("hi", channels=["Notifications"])
print 'Done'