
# GEAR Chat


README TODO - See blog post for now.


See the main readme in the repo for installing weave.


## Quickstart

To run the evaluation:

    python gear_eval.py where_to_post


To chat with all the agents:

    python gear_chat.py where_to_post


To chat with a specific agent:

    python test_drive.py gather where_to_post --text "I have a cool photo of the steak I cooked last night."

    python test_drive.py elect where_to_post "
        HAS_PHOTO: [Gathered.COMPLETE] Yes
        FACTUALLY_CORRECT: [Gathered.NO_DATA] Not mentioned
        POST_TOPIC: [Gathered.COMPLETE] The user cooked a steak last night"

    python test_drive.py author where_to_post "I have a cool photo of the steak I cooked last night." --instructions "Tell the user to first post on reddit and then repost on instagram."
    
    python test_drive.py review where_to_post "That looks delicious! You should post it on Reddit first, and then share it on Instagram."


   



