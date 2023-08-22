##
# unused, from Driver
##
# LOGIN_FORM = "b-loginreg__form"
# TWITTER_LOGIN0 = "//a[@class='g-btn m-rounded m-flex m-lg']"
# TWITTER_LOGIN1 = "//a[@class='g-btn m-rounded m-flex m-lg btn-twitter']"
# TWITTER_LOGIN2 = "//a[@class='btn btn-default btn-block btn-lg btn-twitter']"
# TWITTER_LOGIN3 = "//a[@class='g-btn m-rounded m-flex m-lg m-with-icon']"
# USERNAME_XPATH = "//input[@id='username_or_email']"
# PASSWORD_XPATH = "//input[@id='password']"
# SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded']"
# SEND_BUTTON_CLASS2 = "button.g-btn.m-rounded"
# LIVE_BUTTON_CLASS = "b-make-post__streaming-link"
# DISCOUNT_INPUT = "form-control.b-fans__trial__select-wrapper"
# ONLYFANS_PRICE2 = "button.b-chat__btn-set-price"

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

    {
        "name": "rememberMe",
        "xpath": ["//input[@id='remember']"],
        "classes": [],
        "text": [],
        "id": []
    }
]