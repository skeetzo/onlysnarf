#!/usr/bin/python3

# a mess of css references to be cleaned up another time

from OnlySnarf.settings import SETTINGS as settings


##
# new idea

# alt tab until the correct flag is reached ala
# alt tab through on a settings page until the innerHTML text marks the proceeding input

# an alt tab count works on everything
# so transition the elements.py class into providing the correct number of alt tabs or text element to search 
#   for the desired element

# *boom noises*

##


ONLYFANS_HOME_URL = 'https://onlyfans.com/'
ONLYFANS_SETTINGS_URL = "https://onlyfans.com/my/settings"
ONLYFANS_USERS_ACTIVE_URL = "https://onlyfans.com/my/subscribers/active"
SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded']"
SEND_BUTTON_CLASS = "g-btn.m-rounded"
SEND_BUTTON_CLASS2 = "button.g-btn.m-rounded"
LIVE_BUTTON_CLASS = "b-make-post__streaming-link"
TWITTER_LOGIN0 = "//a[@class='g-btn m-rounded m-flex m-lg']"
TWITTER_LOGIN1 = "//a[@class='g-btn m-rounded m-flex m-lg btn-twitter']"
TWITTER_LOGIN2 = "//a[@class='btn btn-default btn-block btn-lg btn-twitter']"
USERNAME_XPATH = "//input[@id='username_or_email']"
PASSWORD_XPATH = "//input[@id='password']"
MESSAGE_INPUT_CLASS = ".form-control.b-chat__message-input"
MESSAGE_CONFIRM = "g-btn.m-rounded.b-chat__btn-submit"
MESSAGE_CONFIRM2 = "button.g-btn.m-rounded.b-chat__btn-submit"
MONTHS_INPUT = "form-control.b-fans__trial__select"
DISCOUNT_INPUT = "form-control.b-fans__trial__select"
DISCOUNT_TEXT = "form-control.b-fans__trial__select"
DISCOUNT_USER_BUTTONS = "g-btn.m-rounded.m-border.m-sm"
DISCOUNT_USER_BUTTON = "g-btn.m-rounded"
DISCOUNT_USERS = "g-btn.m-rounded.m-border.m-sm"
DISCOUNT_USERS_ = "b-users__item.m-fans"
EXPIRATION = "g-btn.m-flat.b-make-post__expire-period-btn"
EXPIRATION2 = "button.g-btn.m-flat.b-make-post__expire-period-btn"
EXPIRATION_PERIODS = "b-make-post__expire__label"
EXPIRATION_PERIODS2 = "button.b-make-post__expire__label"
EXPIRATION_SAVE = "g-btn.m-rounded"
EXPIRATION_SAVE2 = "button.g-btn.m-rounded"
EXPIRATION_SAVE3 = "button.g-btn.m-rounded.js-make-post-poll-duration-save"
EXPIRATION_SAVE4 = "g-btn.m-rounded.js-make-post-poll-duration-save"
EXPIRATION_CANCEL = "g-btn.m-rounded.m-border"
EXPIRATION_CANCEL2 = "button.g-btn.m-rounded.m-border"
ONLYFANS_TWEET = "//label[@for='new_post_tweet_send']"
ONLYFANS_UPLOAD_PHOTO_ID = "fileupload_photo"
ONLYFANS_UPLOAD_MESSAGE_PHOTO_ID = "cm_fileupload_photo"
ONLYFANS_USER_COUNT = "l-sidebar__user-data__item__count"
ONLYFANS_USERS_IDS = "a.g-btn.m-rounded.m-border.m-sm"
ONLYFANS_USERS_STARTEDS = "b-fans__item__list__item"
ONLYFANS_USERS = "g-user-name__wrapper"
ONLYFANS_USERSNAMES = "g-user-username"
ONLYFANS_POST_TEXT_ID = "new_post_text_input"
ONLYFANS_PRICE = "b-chat__btn-set-price"
ONLYFANS_PRICE2 = "button.b-chat__btn-set-price"
ONLYFANS_PRICE_INPUT = "form-control.g-input"
ONLYFANS_PRICE_INPUT2 = ".form-control.g-input"
ONLYFANS_PRICE_INPUT3 = "input.form-control.g-input"
ONLYFANS_PRICE_INPUT4 = "input.form-control.g-input"
ONLYFANS_PRICE_CLICK = "g-btn.m-rounded"
ONLYFANS_PRICE_CLICK2 = "button.g-btn.m-rounded"
ONLYFANS_CHAT_URL = "https://onlyfans.com/my/chats/chat"
ONLYFANS_UPLOAD_BUTTON = "g-btn.m-rounded.m-border"
ONLYFANS_MESSAGE_SEND_BUTTON = "g-btn.m-rounded.b-chat__btn-submit"
ONLYFANS_MESSAGES_FROM = "m-from-me"
ONLYFANS_MESSAGES_ALL = "b-chat__message__text"
ONLYFANS_MESSAGES = "b-chat__message__text"
ONLYFANS_MORE = "g-btn.m-flat.b-make-post__more-btn"
ONLYFANS_MORE2 = "button.g-btn.m-flat.b-make-post__more-btn"
# ONLYFANS_MORE = "g-btn.m-flat.b-make-post__more-btn.has-tooltip.v-tooltip-open"
SCHEDULE = "g-btn.m-flat.b-make-post__datepicker-btn"
SCHEDULE2 = "button.g-btn.m-flat.b-make-post__datepicker-btn"
SCHEDULE_EXISTING_DATE = "vdatetime-calendar__current--month"
SCHEDULE_EXISTING_DATE6 = "div.vdatetime-calendar__navigation > div.vdatetime-calendar__current--month"
# <div class="vdatetime-calendar__current--month">January 2020</div>
# //*[@id="make_post_form"]/div/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div[2]
SCHEDULE_EXISTING_DATE2 = ".vdatetime-calendar__current--month"
SCHEDULE_EXISTING_DATE3 = "div.vdatetime-calendar__current--month"
SCHEDULE_EXISTING_DATE4 = "vdatetime-popup__date"
SCHEDULE_EXISTING_DATE5 = "div.vdatetime-popup__date"
SCHEDULE_NEXT_MONTH = "vdatetime-calendar__navigation--next"
SCHEDULE_NEXT_MONTH2 = "button.vdatetime-calendar__navigation--next"
SCHEDULE_DAYS = "vdatetime-calendar__month__day"
SCHEDULE_DAYS2 = "button.vdatetime-calendar__month__day"
SCHEDULE_SAVE = "g-btn.m-rounded"
SCHEDULE_SAVE2 = "button.g-btn.m-rounded"
SCHEDULE_HOURS = "vdatetime-time-picker__item.vdatetime-time-picker__item"
SCHEDULE_HOURS2 = "button.vdatetime-time-picker__item.vdatetime-time-picker__item"
SCHEDULE_MINUTES = "vdatetime-time-picker__item"
SCHEDULE_MINUTES2 = "button.vdatetime-time-picker__item"
POLL = "g-btn.m-flat.b-make-post__voting-btn"
POLL2 = "g-btn.m-flat.b-make-post__voting-btn.has-tooltip"
POLL3 = "button.g-btn.m-flat.b-make-post__voting-btn"
POLL4 = "button.g-btn.m-flat.b-make-post__voting-btn.has-tooltip"
POLL_DURATION = "g-btn.m-flat.b-make-post__voting__duration"
POLL_DURATION2 = "button.g-btn.m-flat.b-make-post__voting__duration"
POLL_DURATION3 = "g-btn.m-rounded.js-make-post-poll-duration-save"
POLL_DURATION4 = "button.g-btn.m-rounded.js-make-post-poll-duration-save"
POLL_ADD_QUESTION = "g-btn.m-flat.new_vote_add_option"
POLL_ADD_QUESTION2 = "button.g-btn.m-flat.new_vote_add_option"
POLL_SAVE = "g-btn.m-rounded"
POLL_SAVE2 = "button.g-btn.m-rounded"
POLL_CANCEL = "b-dropzone__preview__delete"
POLL_INPUT_XPATH = "//input[@class='form-control']"
REMEMBERME_CHECKBOX_XPATH = "//input[@id='remember']"

BALLSBALLS = None
ONLYFANS_ELEMENTS = [
    ### login
    {
        "name": "login",
        "classes": [],
        "text": [],
        "id": [],
        "tabIndex": 2,
        "from": "load"
    },
    # username
    {
        "name": "loginUsername",
        "classes": [],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "login"
    },
    # password
    {
        "name": "loginPassword",
        "classes": [],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "loginUsername"
    },
    {
        "name": "loginCheck",
        "classes": [LIVE_BUTTON_CLASS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ### upload
    # send
    {
        "name": "new_post",
        "classes": [SEND_BUTTON_CLASS, SEND_BUTTON_CLASS2],
        "text": ["Post"],
        "id": [],
        "tabIndex": 30,
        "from": "load"
    },


    # record voice
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "new_post"
    },
    # post price
    {
        "name": "post_price",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 9,
        "from": "new_post"
    },
    # post price cancel
    {
        "name": "post_price_cancel",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "new_post"
    },
    # post price save
    {
        "name": "post_price_save",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 2,
        "from": "new_post"
    },
    # go live
    {
        "name": "go_live",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 12,
        "from": "new_post"
    },
    # 

    # upload image file
    {
        "name": "image_upload",
        "classes": [MESSAGE_CONFIRM2, MESSAGE_CONFIRM],
        "text": [],
        "id": [ONLYFANS_UPLOAD_PHOTO_ID],
        "tabIndex": 11,
        "from": "new_post"
    },
    # show more options # unnecessary w/ tabbing
    # {
    #     "name": "moreOptions",
    #     "classes": [ONLYFANS_MORE, ONLYFANS_MORE2],
    #     "text": [],
    #     "id": [],
    #     "tabIndex": None,
    #     "from": "load"
    # },
    # poll
    {
        "name": "poll",
        "classes": [POLL, POLL2, POLL3, POLL4],
        "text": ["<svg class=\"g-icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-more\" href=\"#icon-more\"></use></svg>"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll cancel
    {
        "name": "pollCancel",
        "classes": [POLL_CANCEL],
        "text": ["Cancel"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll duration
    {
        "name": "pollDuration",
        "classes": [POLL_DURATION, POLL_DURATION2, POLL_DURATION3, POLL_DURATION4],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # duration tabs
    {
        "name": "pollDurations",
        "classes": [EXPIRATION_PERIODS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll save duration
    {
        "name": "pollSave",
        "classes": [POLL_SAVE, POLL_SAVE2],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll add question
    {
        "name": "pollQuestionAdd",
        "classes": [POLL_ADD_QUESTION, POLL_ADD_QUESTION2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    # expiration
    {
        "name": "expirationAdd",
        "classes": [EXPIRATION, EXPIRATION2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration periods (same for duration)
    {
        "name": "expirationPeriods",
        "classes": [EXPIRATION_PERIODS, EXPIRATION_PERIODS2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration save
    {
        "name": "expirationSave",
        "classes": [EXPIRATION_SAVE, EXPIRATION_SAVE2, EXPIRATION_SAVE3, EXPIRATION_SAVE4],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration cancel
    {
        "name": "expirationCancel",
        "classes": [EXPIRATION_CANCEL, EXPIRATION_CANCEL2],
        "text": ["Cancel"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # discount modal for user
    {
        "name": "discountUserButton",
        "classes": [DISCOUNT_USER_BUTTON],
        "text": ["Apply"],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # discount save for user
    {
        "name": "discountUsers",
        "classes": [DISCOUNT_USERS_],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },

    ## price
    # price add
    {
        "name": "priceClick",
        "classes": [ONLYFANS_PRICE_CLICK, ONLYFANS_PRICE_CLICK2],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # price enter (adds .00)
    {
        "name": "priceEnter",
        "classes": [ONLYFANS_PRICE_INPUT, ONLYFANS_PRICE_INPUT2, ONLYFANS_PRICE_INPUT3, ONLYFANS_PRICE_INPUT4],
        "text": ["Free"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    # schedule add
    {
        "name": "scheduleAdd",
        "classes": [SCHEDULE, SCHEDULE2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule next month
    {
        "name": "scheduleNextMonth",
        "classes": [SCHEDULE_NEXT_MONTH, SCHEDULE_NEXT_MONTH2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule date
    {
        "name": "scheduleDate",
        "classes": [SCHEDULE_EXISTING_DATE, SCHEDULE_EXISTING_DATE6, SCHEDULE_EXISTING_DATE2, SCHEDULE_EXISTING_DATE3, SCHEDULE_EXISTING_DATE4, SCHEDULE_EXISTING_DATE5],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule minutes
    {
        "name": "scheduleMinutes",
        "classes": [SCHEDULE_MINUTES, SCHEDULE_MINUTES2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule hours
    {
        "name": "scheduleHours",
        "classes": [SCHEDULE_HOURS, SCHEDULE_HOURS2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule days
    {
        "name": "scheduleDays",
        "classes": [SCHEDULE_DAYS, SCHEDULE_DAYS2],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule save
    {
        "name": "scheduleSave",
        "classes": [SCHEDULE_SAVE, SCHEDULE_SAVE2],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    ### message
    # message enter text
    {
        "name": "messageText",
        "classes": [MESSAGE_INPUT_CLASS],
        "text": [],
        "id": [],
        "tabIndex": 14,
        "from": "load"
    },
    # message upload image
    {
        "name": "uploadImageMessage",
        "classes": [MESSAGE_CONFIRM],
        "text": [],
        "id": [ONLYFANS_UPLOAD_MESSAGE_PHOTO_ID],
        "tabIndex": None, # can't find
        "from": "load"
    },
    # upload error window close
    # tab probably closes error windows...
    {
        "name": "errorUpload",
        "classes": [EXPIRATION_CANCEL, EXPIRATION_CANCEL2],
        "text": ["Close"],
        "id": [],
        "tabIndex": None,
        "from": "new_message"
    },
    # messages all
    {
        "name": "messagesAll",
        "classes": [ONLYFANS_MESSAGES_ALL],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # messages from user
    {
        "name": "messagesFrom",
        "classes": [ONLYFANS_MESSAGES_FROM],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # messages to user
    {
        "name": "usersUsernames",
        "classes": [ONLYFANS_USERSNAMES],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ## Users
    # users
    {
        "name": "usersUsers",
        "classes": [ONLYFANS_USERS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users started dates
    {
        "name": "usersStarteds",
        "classes": [ONLYFANS_USERS_STARTEDS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users ids
    {
        "name": "usersIds",
        "classes": [ONLYFANS_USERS_IDS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users count
    {
        "name": "usersCount",
        "classes": [ONLYFANS_USER_COUNT],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users discount buttons
    {
        "name": "discountUserButtons",
        "classes": [DISCOUNT_USER_BUTTONS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },

    ## Settings ##

    ## Account
    # cover image enter
    {
        "name": "coverImage",
        "classes": ["b-user-panel__cover__img"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # cover image cancel
    {
        "name": "coverImageCancel",
        "classes": [],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # profile photo
    {
        "name": "profilePhoto",
        "classes": ["g-btn.m-rounded.m-sm.m-border"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # display name
    {
        "name": "displayName",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": 7, # left
        "from": "load"
    },
    # subscription price
    {
        "name": "subscriptionPrice",
        "classes": ["form-control.g-input","classname"],
        "text": [],
        "id": [],
        "tabIndex": 6, # left
        "from": "load"
    },
    # ADD reward for subscriber referrals
    # about
    {
        "name": "about",
        "classes": ["form-control.g-input.unlimsize"],
        "text": [],
        "id": [],
        "tabIndex": 5, # left
        "from": "load"
    },
    # location
    {
        "name": "location",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": 4, # left
        "from": "load"
    },
    # website url
    {
        "name": "websiteURL",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": 3, # left
        "from": "load"
    },

    ## Advanced
    # username
    # BLANK
    # email
    {
        "name": "email",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": 3, # left
        "from": "load"
    },
    # username
    {
        "name": "username",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": 4, # left
        "from": "load"
    },
    # connect other onlyfans accounts username enter area
    # BLANK
    # password
    {
        "name": "password",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # password 2x
    {
        "name": "newPassword",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # confirm new password
    {
        "name": "confirmPassword",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },

    ## Notifications
    # push notifications
    # BLANK
    # email notifications
    {
        "name": "emailNotifs",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new referral email
    {
        "name": "emailNotifsNewReferral",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new stream email
    {
        "name": "emailNotifsNewStream",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new subscriber email
    {
        "name": "emailNotifsNewSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new tip email
    {
        "name": "emailNotifsNewSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new renewal email
    {
        "name": "emailNotifsNewSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },

    {
        "name": "emailNotifsNewTip",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    #
    {
        "name": "emailNotifsRenewal",
        "classes": ["b-input-radio"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new likes summary
    {
        "name": "emailNotifsNewLikes",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new posts summary
    {
        "name": "emailNotifsNewPosts",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new private message summary
    {
        "name": "emailNotifsNewPrivMessages",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # telegram bot button
    # BLANK
    # site notifications
    {
        "name": "siteNotifs",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new comment notification
    {
        "name": "siteNotifsNewComment",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new favorite notification
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # discounts from users i've used to follow notification
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new subscriber notification
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # new tip notification
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # toast notification new comment
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # toast notification new favorite
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # toast notification new subscriber
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # toast notification new tip
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ## Security
    # two step toggle
    # BLANK
    # fully private profile
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # enable comments
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # show fans count on profile
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # show posts tips summary
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # public friends list
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # geo blocking
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 4, # left
        "from": "load"
    },
    # ip blocking
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 3, # left
        "from": "load"
    },
    # watermarks photos
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # watermarks video
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # watermarks text
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 2,
        "from": "load"
    },
    ####### save changes may be the same for each
    ## Story
    # allow message replies - nobody
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # allow message replies - subscribers
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # show story for - everyone
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # show story for - subscribers
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ## Other
    # obs server
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 12, # left
        "from": "load"
    },
    # obs key
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 11, # left
        "from": "load"
    },
    # welcome chat message toggle
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": 10, 
        "from": "load"
    },
    # then same pattern for message enter text or add stuff and price
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None, # lefts
        "from": "load"
    },
    # save button for welcome chat message
    {
        "name": "BALLS",
        "classes": [BALLSBALLS],
        "text": [],
        "id": [],
        "tabIndex": None, # left
        "from": "load"
    },

]

# represents elements the webdriver sortof looks for
class Element:
    def __init__(self, name=None, classes=[], text=[], id=[]):
        self.name = name
        self.classes = classes
        self.text = text
        self.id = id

    def getClass(self):
        if self.classes and len(self.classes) > 0:
            return self.classes[0]
        return ""

    def getClasses(self):
        return self.classes

    def getText(self):
        if self.text and len(self.text) > 0:
            return self.text[0]
        return ""

    def getTexts(self):
        return self.text

    def getId(self):
        if self.id and len(self.id) > 0:
            return self.id[0]

    @staticmethod
    def get_element_by_name(name):
        settings.devPrint("getting element: {}".format(name))
        if name == None:
            settings.maybePrint("Error: Missing Element Name")
            return None
        global ONLYFANS_ELEMENTS
        for element in ONLYFANS_ELEMENTS:
            # element = Element(name=element["name"], classes=element["classes"], text=element["text"], id=element["id"])
            if str(element["name"]) == str(name):
                settings.devPrint("prepped ele: {}".format(element["name"]))
                return Element(name=element["name"], classes=element["classes"], text=element["text"], id=element["id"])
        settings.devPrint("Warning: Missing Element Fetch - {}".format(name))
        return None