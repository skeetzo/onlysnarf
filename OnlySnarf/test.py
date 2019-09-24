
    # ### Promotion ###
    print('TESTING: Promotion')
    response = apply_promotion()
    if not response or response == None:
        print("Error: Failed to apply promotion")
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    return

    # ### Gallery ###
    # print('TESTING: Gallery x 10')
    # for i in range(10):
    #     release_gallery()
    #     time.sleep(10)
    #     reset = OnlySnarf.reset()
    #     if not reset:
    #         return print("Error: Failed to Reset")
    # return sys.exit(0)
    # #######################

    # ### Message ###
    # response = download_random_image()
    # if not response or response == None:
        # print("Error: Missing Image")
        # return
    # successful_message = OnlySnarf.message(choice="all", message="random tease :P", image=response[1], price="5.00")
    # message(choice="recent", message="8=======D", image=response[1], price="50.00")
    # if successful_message:
        # Google.move_file(response[2])
    # else:
        # print("Error: Failed to Send Message")
    # #######################
    # ### Exit Gracefully ###
    # OnlySnarf.exit()
    # return
    # #######################

    # ### Users ###
    print('TESTING: Users')
    users = OnlySnarf.get_users()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    return
    #######################

    # ### Chat Logs ###
    # print('TESTING: Chat Logs')
    # OnlySnarf.update_chat_logs()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    # #######################
    # ### Exit Gracefully ###
    # OnlySnarf.exit()
    # return
    # #######################
    
    # ### Image ###
    # print('TESTING: Image')
    # release_image()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    # ### Gallery ###
    # print('TESTING: Gallery')
    # release_gallery()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    # ### Performer ###
    # print('TESTING: Performer')
    # release_performer()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    ### Scene ###
    # print('TESTING: Scene')
    # release_scene()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    # ### Video ###
    # print('TESTING: Video')
    # release_video()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
    #     return print("Error: Failed to Reset")
    
    #######################
    ### Exit Gracefully ###
    # OnlySnarf.exit()
    #######################
