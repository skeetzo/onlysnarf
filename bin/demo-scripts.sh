##################
## Demo Scripts ##
##################

# Discount
snarf -debug discount -user random -amount max -months max

# Message
snarf -debug message -user random -text shnarf! -price min ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Post
snarf -debug post -text "shnarf" -tags "suck" -tags "my" -tags "balls" -performers "yourmom" -performers  "yourdad" ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Poll
snarf -debug post -text shnarff! -question "sharnf shnarf?" -question "shnarf shhhnarff snarf?" -duration min

# Schedule
snarf -debug post -text shnarff! -schedule "10/31/2022 16:20:00"

# User
snarf -debug users

snarf -debug -browser brave users

snarf post -text "shnarff?" -question "yes" -question "maybe?" -question "no" -question "double shnarf" -duration "min"

# debug remote path upload
snarf -debug -debug-delay -verbose -verbose -verbose -show post -text "shnarrff" "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"