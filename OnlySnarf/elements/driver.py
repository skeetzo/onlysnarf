# general driver elements

ELEMENTS = [
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
        "classes": ["b-make-post__streaming-link"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ### upload
    # send
    {
        "name": "new_post",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Post"],
        "id": [],
        "tabIndex": 30,
        "from": "load"
    },


    # record voice
    {
        "name": "recordVoice",
        "classes": [None],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "new_post"
    },
    # post price
    {
        "name": "post_price",
        "classes": [None],
        "text": [],
        "id": [],
        "tabIndex": 9,
        "from": "new_post"
    },
    # post price cancel
    {
        "name": "post_price_cancel",
        "classes": [None],
        "text": [],
        "id": [],
        "tabIndex": 1,
        "from": "new_post"
    },
    # post price save
    {
        "name": "post_price_save",
        "classes": [None],
        "text": [],
        "id": [],
        "tabIndex": 2,
        "from": "new_post"
    },
    # go live
    {
        "name": "go_live",
        "classes": [None],
        "text": [],
        "id": [],
        "tabIndex": 12,
        "from": "new_post"
    },
    # 

    # upload image file
    {
        "name": "image_upload",
        "classes": ["button.g-btn.m-rounded.b-chat__btn-submit", "g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": ["fileupload_photo"],
        "tabIndex": 11,
        "from": "new_post"
    },
    # show more options # unnecessary w/ tabbing
    # {
    #     "name": "moreOptions",
    #     "classes": ["g-btn.m-flat.b-make-post__more-btn", "button.g-btn.m-flat.b-make-post__more-btn"],
    #     "text": [],
    #     "id": [],
    #     "tabIndex": None,
    #     "from": "load"
    # },
    # poll
    {
        "name": "poll",
        "classes": ["g-btn.m-flat.b-make-post__voting-btn", "g-btn.m-flat.b-make-post__voting-btn.has-tooltip", "button.g-btn.m-flat.b-make-post__voting-btn", "button.g-btn.m-flat.b-make-post__voting-btn.has-tooltip"],
        "text": ["<svg class=\"g-icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-more\" href=\"#icon-more\"></use></svg>"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll cancel
    {
        "name": "pollCancel",
        "classes": ["b-dropzone__preview__delete"],
        "text": ["Cancel"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll duration
    {
        "name": "pollDuration",
        "classes": ["g-btn.m-flat.b-make-post__voting__duration", "button.g-btn.m-flat.b-make-post__voting__duration", "g-btn.m-rounded.js-make-post-poll-duration-save", "button.g-btn.m-rounded.js-make-post-poll-duration-save"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # duration tabs
    {
        "name": "pollDurations",
        "classes": ["b-make-post__expire__label"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll save duration
    {
        "name": "pollSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # poll add question
    {
        "name": "pollQuestionAdd",
        "classes": ["g-btn.m-flat.new_vote_add_option", "button.g-btn.m-flat.new_vote_add_option"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    # expiration
    {
        "name": "expirationAdd",
        "classes": ["g-btn.m-flat.b-make-post__expire-period-btn", "button.g-btn.m-flat.b-make-post__expire-period-btn"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration periods (same for duration)
    {
        "name": "expirationPeriods",
        "classes": ["b-make-post__expire__label", "button.b-make-post__expire__label"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration save
    {
        "name": "expirationSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded", "button.g-btn.m-rounded.js-make-post-poll-duration-save", "g-btn.m-rounded.js-make-post-poll-duration-save"],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # expiration cancel
    {
        "name": "expirationCancel",
        "classes": ["g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],
        "text": ["Cancel"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # discount modal for user
    {
        "name": "discountUserButton",
        "classes": ["g-btn.m-rounded"],
        "text": ["Apply"],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # discount save for user
    {
        "name": "discountUsers",
        "classes": ["b-users__item.m-fans"],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },

    ## price
    # price add
    {
        "name": "priceClick",
        "classes": ["b-chat__btn-set-price", "button.g-btn.m-rounded"],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # price enter (adds .00)
    {
        "name": "priceEnter",
        "classes": ["form-control.g-input", ".form-control.g-input", "input.form-control.g-input", "input.form-control.g-input"],
        "text": ["Free"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    # schedule add
    {
        "name": "scheduleAdd",
        "classes": ["g-btn.m-flat.b-make-post__datepicker-btn", "button.g-btn.m-flat.b-make-post__datepicker-btn"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule next month
    {
        "name": "scheduleNextMonth",
        "classes": ["vdatetime-calendar__navigation--next", "button.vdatetime-calendar__navigation--next"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule date
    {
        "name": "scheduleDate",
        "classes": ["vdatetime-calendar__current--month", "div.vdatetime-calendar__navigation > div.vdatetime-calendar__current--month", ".vdatetime-calendar__current--month", "div.vdatetime-calendar__current--month", "vdatetime-popup__date", "div.vdatetime-popup__date"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule minutes
    {
        "name": "scheduleMinutes",
        "classes": ["vdatetime-time-picker__item", "button.vdatetime-time-picker__item"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule hours
    {
        "name": "scheduleHours",
        "classes": ["vdatetime-time-picker__item.vdatetime-time-picker__item", "button.vdatetime-time-picker__item.vdatetime-time-picker__item"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule days
    {
        "name": "scheduleDays",
        "classes": ["vdatetime-calendar__month__day", "button.vdatetime-calendar__month__day"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },
    # schedule save
    {
        "name": "scheduleSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Save"],
        "id": [],
        "tabIndex": None,
        "from": "new_post"
    },

    ### message
    # message enter text
    {
        "name": "messageText",
        "classes": [".form-control.b-chat__message-input"],
        "text": [],
        "id": [],
        "tabIndex": 14,
        "from": "load"
    },
    # message upload image
    {
        "name": "uploadImageMessage",
        "classes": ["g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": ["cm_fileupload_photo"],
        "tabIndex": None, # can't find
        "from": "load"
    },
    # upload error window close
    # tab probably closes error windows...
    {
        "name": "errorUpload",
        "classes": ["g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],
        "text": ["Close"],
        "id": [],
        "tabIndex": None,
        "from": "new_message"
    },
    # messages all
    {
        "name": "messagesAll",
        "classes": ["b-chat__message__text"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # messages from user
    {
        "name": "messagesFrom",
        "classes": ["m-from-me"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # messages to user
    {
        "name": "usersUsernames",
        "classes": ["g-user-username"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    ## Users
    # users
    {
        "name": "usersUsers",
        "classes": ["g-user-name__wrapper"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users started dates
    {
        "name": "usersStarteds",
        "classes": ["b-fans__item__list__item"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users ids
    {
        "name": "usersIds",
        "classes": ["a.g-btn.m-rounded.m-border.m-sm"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users count
    {
        "name": "usersCount",
        "classes": ["l-sidebar__user-data__item__count"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    },
    # users discount buttons
    {
        "name": "discountUserButtons",
        "classes": ["g-btn.m-rounded.m-border.m-sm"],
        "text": [],
        "id": [],
        "tabIndex": None,
        "from": "load"
    }

]