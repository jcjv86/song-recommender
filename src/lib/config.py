# Feel free to configure this file to your needs.
# All variables have default values except for Spotify Credentials and source database.
# Please make sure to provide these values or the script won't work.

# Set client_id and client_secret
client_id = ''
client_secret = ''

# Exported files absolute path (final files destination folder, will be deleted if it already exists and then created, by default in script folder).
exported_files = './exported_files'

# Path and name of the logs file - default status.log, will be created in script folder - can be accessed later with: grep "INFO" status.log | tail -2
log_file = 'status.log'

# Set timer between each API call.
# ////// CAUTION //////
# You shouldn't make more than 10 calls in a 30 sec window to avoid getting banned temporarily'
timer = 3

# Original dataframe with songs and artists name that you want to get Song ID and features for.
source = ''
