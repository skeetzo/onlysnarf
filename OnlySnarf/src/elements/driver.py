# general driver elements

ELEMENTS = [
    ### login
    {
        "name": "login",
        "classes": [],
        "text": [],
        "id": []
    },
    # username
    {
        "name": "loginUsername",
        "classes": [],
        "text": [],
        "id": []
    },
    # password
    {
        "name": "loginPassword",
        "classes": [],
        "text": [],
        "id": []
    },
    {
        "name": "loginCheck",
        "classes": ["b-make-post__streaming-link"],
        "text": [],
        "id": []
    },
    ### upload
    # send
    {
        "name": "new_post",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Post"],
        "id": []
    },


    # record voice
    {
        "name": "recordVoice",
        "classes": [None],
        "text": [],
        "id": []
    },
    # post price
    {
        "name": "post_price",
        "classes": [None],
        "text": [],
        "id": []
    },
    # post price cancel
    {
        "name": "post_price_cancel",
        "classes": [None],
        "text": [],
        "id": []
    },
    # post price save
    {
        "name": "post_price_save",
        "classes": [None],
        "text": [],
        "id": []
    },
    # go live
    {
        "name": "go_live",
        "classes": [None],
        "text": [],
        "id": []
    },
    # upload image file
    {
        "name": "image_upload",
        "classes": ["button.g-btn.m-rounded.b-chat__btn-submit", "g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": ["fileupload_photo"]
    },
    # show more options # unnecessary w/ tabbing
    {
        "name": "moreOptions",
        "classes": ["g-btn.m-flat.b-make-post__more-btn.has-tooltip", "g-btn.m-flat.b-make-post__more-btn", "button.g-btn.m-flat.b-make-post__more-btn"],
        "text": [],
        "id": []
    },
    
    # poll
    {
        "name": "poll",
        "classes": ["g-btn.m-flat.b-make-post__voting-btn", "g-btn.m-flat.b-make-post__voting-btn.has-tooltip", "button.g-btn.m-flat.b-make-post__voting-btn", "button.g-btn.m-flat.b-make-post__voting-btn.has-tooltip"],
        "text": ["<svg class=\"g-icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-more\" href=\"#icon-more\"></use></svg>"],
        "id": []
    },
    # expire add
    {
        "name": "expiresAdd",
        "classes": ["b-make-post__expire-period-btn"],
        "text": ["Save"],
        "id": []
    },
    {
        "name": "expiresPeriods",
        "classes": ["b-make-post__expire__label"],
        "text": [],
        "id": []
    },
    {
        "name": "expiresSave",
        "classes": ["g-btn.m-rounded"],
        "text": ["Save"],
        "id": []
    },
    {
        "name": "expiresCancel",
        "classes": ["g-btn.m-rounded.m-border"],
        "text": ["Cancel"],
        "id": []
    },
    # poll cancel
    {
        "name": "pollCancel",
        "classes": ["b-dropzone__preview__delete"],
        "text": ["Cancel"],
        "id": []
    },
    # poll duration
    {
        "name": "pollDuration",
        "classes": ["g-btn.m-flat.b-make-post__voting__duration", "button.g-btn.m-flat.b-make-post__voting__duration", "g-btn.m-rounded.js-make-post-poll-duration-save", "button.g-btn.m-rounded.js-make-post-poll-duration-save"],
        "text": [],
        "id": []
    },
    # duration tabs
    {
        "name": "pollDurations",
        "classes": ["b-make-post__expire__label"],
        "text": [],
        "id": []
    },
    # poll save duration
    {
        "name": "pollSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Save"],
        "id": []
    },
    # poll add question
    {
        "name": "pollQuestionAdd",
        "classes": ["g-btn.m-flat.new_vote_add_option", "button.g-btn.m-flat.new_vote_add_option"],
        "text": [],
        "id": []
    },

    # expiration
    {
        "name": "expirationAdd",
        "classes": ["g-btn.m-flat.b-make-post__expire-period-btn", "button.g-btn.m-flat.b-make-post__expire-period-btn"],
        "text": [],
        "id": []
    },
    # expiration periods (same for duration)
    {
        "name": "expirationPeriods",
        "classes": ["b-make-post__expire__label", "button.b-make-post__expire__label"],
        "text": [],
        "id": []
    },
    # expiration save
    {
        "name": "expirationSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded", "button.g-btn.m-rounded.js-make-post-poll-duration-save", "g-btn.m-rounded.js-make-post-poll-duration-save"],
        "text": ["Save"],
        "id": []
    },
    # expiration cancel
    {
        "name": "expirationCancel",
        "classes": ["g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],
        "text": ["Cancel"],
        "id": []
    },
    # discount modal for user
    {
        "name": "discountUserButton",
        "classes": ["g-btn.m-rounded"],
        "text": ["Apply"],
        "id": []
    },
    # discount save for user
    {
        "name": "discountUsers",
        "classes": ["b-users__item.m-fans"],
        "text": ["Save"],
        "id": []
    },

    ## price
    # price add
    {
        "name": "priceClick",
        "classes": ["g-btn.m-rounded"], # "b-chat__btn-set-price", "button.g-btn.m-rounded"
        "text": ["Save"],
        "id": []
    },
    # price enter (adds .00)
    {
        "name": "priceEnter",
        "classes": ["form-control.g-input", ".form-control.g-input", "input.form-control.g-input", "input.form-control.g-input"],
        "text": ["Free"],
        "id": []
    },

    # schedule add
    {
        "name": "scheduleAdd",
        "classes": ["g-btn.m-flat.b-make-post__datepicker-btn", "button.g-btn.m-flat.b-make-post__datepicker-btn"],
        "text": [],
        "id": []
    },
    # schedule next month
    {
        "name": "scheduleNextMonth",
        "classes": ["vdatetime-calendar__navigation--next", "button.vdatetime-calendar__navigation--next"],
        "text": [],
        "id": []
    },
    # schedule date
    {
        "name": "scheduleDate",
        "classes": ["vdatetime-calendar__current--month", "div.vdatetime-calendar__navigation > div.vdatetime-calendar__current--month", ".vdatetime-calendar__current--month", "div.vdatetime-calendar__current--month", "vdatetime-popup__date", "div.vdatetime-popup__date"],
        "text": [],
        "id": []
    },
    # schedule minutes
    {
        "name": "scheduleMinutes",
        "classes": ["vdatetime-time-picker__item", "button.vdatetime-time-picker__item"],
        "text": [],
        "id": []
    },
    # schedule hours
    {
        "name": "scheduleHours",
        "classes": ["vdatetime-time-picker__item.vdatetime-time-picker__item", "button.vdatetime-time-picker__item.vdatetime-time-picker__item"],
        "text": [],
        "id": []
    },
    # schedule days
    {
        "name": "scheduleDays",
        "classes": ["vdatetime-calendar__month__day", "button.vdatetime-calendar__month__day"],
        "text": [],
        "id": []
    },
    # schedule save
    {
        "name": "scheduleSave",
        "classes": ["g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Save"],
        "id": []
    },

    ### message
    # message enter text
    {
        "name": "messageText",
        "classes": [".form-control.b-chat__message-input"],
        "text": [],
        "id": []
    },
    # message upload image
    {
        "name": "uploadImageMessage",
        "classes": ["g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": ["fileupload_photo"]
    },
    # upload error window close
    # tab probably closes error windows...
    {
        "name": "errorUpload",
        "classes": ["g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],
        "text": ["Close"],
        "id": []
    },
    # messages all
    {
        "name": "messagesAll",
        "classes": ["b-chat__message__text"],
        "text": [],
        "id": []
    },
    # messages from user
    {
        "name": "messagesFrom",
        "classes": ["m-from-me"],
        "text": [],
        "id": []
    },

    ## Users
    {
        "name": "usersUsernames",
        "classes": ["g-user-username"],
        "text": [],
        "id": []
    },
    # users
    {
        "name": "usersUsers",
        "classes": ["g-user-name__wrapper", "b-username"],
        "text": [],
        "id": ["profileUrl"]
    },
    # users started dates
    {
        "name": "usersStarteds",
        "classes": ["b-fans__item__list__item"],
        "text": [],
        "id": []
    },
    # users ids
    {
        "name": "usersIds",
        "classes": ["a.g-btn.m-rounded.m-border.m-sm", "a.g-button.m-rounded.m-border.m-profile.m-with-icon.m-message-btn"],
        "text": [],
        "id": []
    },
    # users count
    {
        "name": "usersCount",
        "classes": ["l-sidebar__user-data__item__count", "b-tabs__nav__item.m-current"],
        "text": [],
        "id": []
    },
    {
        "name": "followingCount",
        "classes": ["b-tabs__nav__item.m-current"],
        "text": [],
        "id": []
    },
    # users discount buttons
    {
        "name": "discountUserButtons",
        "classes": ["g-btn.m-rounded.m-border.m-sm"],
        "text": [],
        "id": []
    },
    {
        "name": "newMessage",
        "classes": ["g-page__header__btn.b-chats__btn-new.has-tooltip"],
        "text": [],
        "href": ["/my/chats/send"],
        "id": [],
    },
    {
        "name": "messageAll",
        "classes": ["g-btn__text"],
        "text": ["Fans"],
        "id": [],
    },
    {
        "name": "messageRecent",
        "classes": ["g-btn__text"],
        "text": ["Recent"],
        "id": [],
    },
    {
        "name": "messageFavorite",
        "classes": ["g-btn__text"],
        "text": ["FAVORITE"],
        "id": [],
    },
    {
        "name": "messageRenewers",
        "classes": ["g-btn__text"],
        "text": ["Renew"],
        "id": [],
    },
    {
        "name": "promotionalTrial",
        "classes": ["g.btn.m-rounded.m-sm"],
        "text": ["Create new trial link"],
        "id": [],
    },
    {
        "name": "promotionalTrialCount",
        "classes": [],
        "text": [],
        "id": ["trial-count-select"],
    },
    {
        "name": "promotionalTrialExpiration",
        "classes": [],
        "text": [],
        "id": ["trial-expiration-select"],
    },
    {
        "name": "promotionalTrialDuration",
        "classes": [],
        "text": [],
        "id": ["promo-campaign-period-select"],
    },
    {
        "name": "promotionalTrialConfirm",
        "classes": ["g-btn.m-rounded"],
        "text": ["Create"],
        "id": [],
    },
    {
        "name": "promotionalTrialCancel",
        "classes": ["g-btn.m-rounded.m-border"],
        "text": ["Cancel"],
        "id": [],
    },
    {
        "name": "promotionalTrialLink",
        "classes": ["g.btn.m-rounded"],
        "text": ["Copy trial link"],
        "id": [],
    },
    {
        "name": "userOptions",
        "classes": ["btn.dropdown-toggle.btn-link"],
        "text": [],
        "id": ["__BVID__56__BV_toggle_"],
    },
    {
        "name": "discountUser",
        "classes": ["button"],
        "text": ["Give user a discount"],
        "id": [],
    },

    {
        "name": "promotionalTrialExpirationUser",
        "classes": [],
        "text": [],
        "id": ["trial-expire-select"],
    },
    {
        "name": "promotionalTrialDurationUser",
        "classes": [],
        "text": [],
        "id": ["trial-period-select"],
    },
    {
        "name": "promotionalTrialMessageUser",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": [],
    },
    {
        "name": "promotionalTrialApply",
        "classes": ["g-btn.m-rounded"],
        "text": ["Apply"],
        "id": [],
    },
    {
        "name": "promotionalTrialCancel",
        "classes": ["g-btn.m-rounded.m-border"],
        "text": ["Cancel"],
        "id": [],
    },
    {
        "name": "numberOfPosts",
        "classes": ["b-profile__actions__count"],
        "text": [],
        "id": [],
    }


]