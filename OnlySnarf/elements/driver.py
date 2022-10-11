# general driver elements

ELEMENTS = [

    {
        "name": "sendButton",
        "classes": ["g-btn.m-rounded"],
        "text": [],
        "id": []
    },
    
    {
        "name": "enterText",
        "classes": [],
        "text": [],
        "id": ["new_post_text_input"]
    },

    {
        "name": "enterMessage",
        "classes": ["b-chat__message__text"],
        "text": [],
        "id": []
    },

    {
        "name": "discountUserPromotion",
        "classes": ["g-btn.m-rounded.m-border.m-sm"],
        "text": [],
        "id": []
    },

    {
        "name": "tweet",
        "xpath": ["//label[@for='new_post_tweet_send']"],
        "classes": [],
        "text": [],
        "id": []
    },

    {
        "name": "pollInput",
        "xpath": ["//input[@class='form-control']"],
        "classes": [],
        "text": [],
        "id": []
    },

    {
        "name": "new_message",
        "classes": ["g-btn.m-rounded.b-chat__btn-submit"],
        "text": ["Send"],
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
        "classes": ["attach_file"],
        "text": [],
        "id": ["attach_file_photo"]
    },
    # show more options # unnecessary w/ tabbing
    {
        "name": "moreOptions",
        "classes": ["button.g-btn.m-flat.b-make-post__more-btn"],
        "text": [],
        "id": []
    },
    
    # poll
    {
        "name": "poll",
        "classes": ["g-btn.m-flat.m-gray.m-with-round-hover.m-size-md-hover.m-default-icon-size.m-reset-width.has-tooltip", "g-btn.m-flat.b-make-post__voting-btn", "g-btn.m-flat.b-make-post__voting-btn.has-tooltip", "button.g-btn.m-flat.b-make-post__voting-btn", "button.g-btn.m-flat.b-make-post__voting-btn.has-tooltip"],
        "text": [],
        "id": ["icon-quiz"]
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
        "classes": ["b-tabs__nav__text", "b-make-post__expire__label"],
        "text": [],
        "id": []
    },
    {
        "name": "listSingleSave",
        "classes": ["g-btn.m-transparent-bg"],
        "text": ["Close"],
        "id": []
    },
    {
        "name": "expiresSave",
        "classes": ["g-btn.m-transparent-bg", "g-btn.m-rounded"],
        "text": ["Save"],
        "id": []
    },
    {
        "name": "expiresCancel",
        "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-transparent-bg", "g-btn.m-rounded.m-border"],
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
        "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width"],
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
    
    {
        "name": "listSave",
        "classes": ["g-btn.m-rounded.m-sm-width"],
        "text": ["Add"],
        "id": []
    },

    ## price
    # price add
    {
        "name": "priceClick",
        "classes": ["g-btn.m-flat.has-tooltip", "g-btn.m-flat.m-gray.m-with-round-hover.m-size-md-hover.m-default-icon-size.m-reset-width"],
        "text": [],
        "id": []
    },
    {
        "name": "priceSave",
        "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-transparent-bg", "g-btn.m-rounded"], # "b-chat__btn-set-price", "button.g-btn.m-rounded"
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
        "classes": ["vdatetime-time-picker__item", "button.vdatetime-time-picker__item", "vdatetime-time-picker__item.vdatetime-time-picker__item--selected"],
        "text": [],
        "id": []
    },
    # schedule hours
    {
        "name": "scheduleHours",  
        "classes": ["vdatetime-time-picker__list--hours", "vdatetime-time-picker__item.vdatetime-time-picker__item", "button.vdatetime-time-picker__item.vdatetime-time-picker__item"],
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
    # schedule next
    {
        "name": "scheduleNext",
        "classes": ["g-btn.m-flat.m-reset-width.m-btn-gaps", "g-btn.m-transparent-bg", "g-btn.m-transparent-bg.m-no-uppercase", "g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["Next"],
        "id": []
    },
    # schedule save
    {
        "name": "scheduleSave",
        "classes": ["g-btn.m-transparent-bg", "g-btn.m-rounded", "button.g-btn.m-rounded"],
        "text": ["OK"],
        "id": []
    },
    # schedule cancel
    {
        "name": "scheduleCancel",
        "classes": ["g-btn.m-transparent-bg", "custom-datepicker-button-cancel", "button.g-btn.m-rounded"],
        "text": ["Cancel"],
        "id": []
    },
    # schedule am/pm
    {
        "name": "scheduleAMPM",
        "classes": ["vdatetime-time-picker__item.vdatetime-time-picker__item--selected"],
        "text": [],
        "id": []
    },

    ### message
    # message enter text
    {
        "name": "messageText",
        "classes": ["form-control.b-make-post__text-input", ".form-control.b-chat__message-input"],
        "text": [],
        "id": []
    },
    # message upload image
    {
        "name": "uploadMessageConfirm",
        "classes": ["g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": ["fileupload_photo"]
    },

    # upload error window close
    # tab probably closes error windows...
    {
        "name": "errorUpload",
        "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-transparent-bg", "g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],
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
        "classes": ["m-from-me","b-chat__message.m-from-me"],
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
        "classes": ["g-btn.m-rounded.m-lg.m-flex.m-with-icon.m-uppercase"],
        "text": ["create new free trial link"],
        "id": [],
    },
    {
        "name": "promotionalCampaignAmount",
        "classes": ["form-control.b-fans__trial__select"],
        "text": ["promo-campaign-discount-percent-select"],
        "id": [],
    },
    {
        "name": "promotionalCampaign",
        "classes": ["g-btn.m-rounded.m-block.m-uppercase"],
        "text": [" Add a promotional campaign "],
        "id": [],
    },
    {
        "name": "promotionalTrialShow",
        "classes": ["g-box__header.m-icon-title.m-gray-bg"],
        "text": ["Free trial links"],
        "id": [],
    },
    {
        "name": "promotionalCopy",
        "classes": ["g-btn.m-rounded.m-uppercase"],
        "text": ["Copy link to profile"],
        "id": [],
    },
    {
        "name": "promotionalTrialCount",
        "classes": ["form-control.b-fans__trial__select"],
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
        "name": "promotionalTrialMessage",
        "classes": ["form-control.g-input"],
        "text": ["Type a message to users (optional)"],
        "id": [],
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
        "name": "postCancel",
        "classes": ["m-btn-clear-draft.g-btn.m-border.m-rounded.m-sm-width.m-reset-width"],
        "text": ["Clear"],
        "id": [],
    },


    {
        "name": "userOptions",
        "classes": ["btn.dropdown-toggle.btn-link"],
        "text": [],
        "id": ["__BVID__56__BV_toggle_"],
    },

    # save discount for user
    {
        "name": "discountUserButton",
        "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-rounded"],
        "text": ["Apply"],
        "id": []
    },
    # discount save for user
    # {
    #     "name": "discountUsers",
    #     "classes": ["b-users__item.m-fans"],
    #     "text": ["Save"],
    #     "id": []
    # },

    {
        "name": "discountUser",
        "classes": ["b-tabs__nav__text"],
        "text": ["Discount"],
        "id": [],
    },

    {
        "name": "discountUserAmount",
        "classes": ["v-select__selection.v-select__selection--comma"],
        "text": ["% discount"],
        "id": [],
    },

    {
        "name": "discountUserMonths",
        "classes": ["v-select__selection.v-select__selection--comma"],
        "text": [" month"],
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