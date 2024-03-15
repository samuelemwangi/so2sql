import json

question_response = json.loads(r"""[
            {
                "tags": [
                    "python",
                    "tkinter"
                ],
                "owner": {
                    "account_id": 30791979,
                    "reputation": 1,
                    "user_id": 23618434,
                    "user_type": "registered",
                    "profile_image": "https://lh3.googleusercontent.com/a/ACg8ocKDDuamFwtZY3Uoe9t9vCyYxztCVSFJLE2tYL1XTNCn0w=k-s256",
                    "display_name": "Bastian Castillo",
                    "link": "https://stackoverflow.com/users/23618434/bastian-castillo"
                },
                "comment_count": 0,
                "reopen_vote_count": 0,
                "close_vote_count": 0,
                "is_answered": false,
                "view_count": 17,
                "favorite_count": 0,
                "down_vote_count": 0,
                "up_vote_count": 0,
                "answer_count": 1,
                "score": 0,
                "last_activity_date": 1710531204,
                "creation_date": 1710526890,
                "last_edit_date": 1710531204,
                "question_id": 78168946,
                "link": "https://stackoverflow.com/questions/78168946/problem-playing-video-playlist-in-tkinter",
                "title": "Problem playing video playlist in tkinter",
                "body": "<p>i making a program that plays a video when it matches with a word that a person says, if it matches, the video shows in a tkinter label"
            },
            {
                 "tags": [
                    "python"
                ],
                "owner": {
                    "account_id": 30791979,
                    "reputation": 1,
                    "user_id": 23618434,
                    "user_type": "registered",
                    "profile_image": "https://lh3.googleusercontent.com/a/ACg8ocKDDuamFwtZY3Uoe9t9vCyYxztCVSFJLE2tYL1XTNCn0w=k-s256",
                    "display_name": "Bastian Castillo",
                    "link": "https://stackoverflow.com/users/23618434/bastian-castillo"
                },
                "comment_count": 1,
                "reopen_vote_count": 0,
                "close_vote_count": 0,
                "is_answered": false,
                "view_count": 107,
                "favorite_count": 0,
                "down_vote_count": 0,
                "up_vote_count": 0,
                "answer_count": 2,
                "score": 0,
                "last_activity_date": 1710531204,
                "creation_date": 1710526890,
                "last_edit_date": 1710531204,
                "question_id": 78168947,
                "link": "https://stackoverflow.com/questions/78168947/problem-playing-video-playlist-in-tkinter",
                "title": "Problem playing video playlist",
                "body": "<p>i making a program that plays a video when it matches with a word that a person says, if it matches, the video shows</p>"
            }
        ]
    """)

question_data = {
    "items": question_response
}

answers_response = json.loads(r"""
    [
        {
        "owner": {
            "account_id": 8512965,
            "reputation": 15129,
            "user_id": 6382434,
            "user_type": "registered",
            "accept_rate": 75,
            "profile_image": "https://www.gravatar.com/avatar/8e1eef40e44288fb695dbdeb87aeb175?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "LMc",
            "link": "https://stackoverflow.com/users/6382434/lmc"
        },
        "edited": false,
        "score": 1,
        "creation_date": 1710536297,
        "post_id": 78169598,
        "comment_id": 137810190,
        "content_license": "CC BY-SA 4.0",
        "body": "Does this answer your question? <a href=\"https://stackoverflow.com/questions/3445590/subset-filter-rows-in-a-data-frame-based-on-a-condition-in-a-column\">Subset / filter rows in a data frame based on a condition in a column</a>"
        },
        {
        "owner": {
            "account_id": 8512965,
            "reputation": 15129,
            "user_id": 6382434,
            "user_type": "registered",
            "accept_rate": 75,
            "profile_image": "https://www.gravatar.com/avatar/8e1eef40e44288fb695dbdeb87aeb175?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "LMc",
            "link": "https://stackoverflow.com/users/6382434/lmc"
        },
        "edited": false,
        "score": 1,
        "creation_date": 1710536279,
        "post_id": 78169598,
        "comment_id": 137810186,
        "content_license": "CC BY-SA 4.0",
        "body": "This is pseudo code since you have not provided a reproducible example: <code>df[df$age &gt;=25,]</code> (the comma is not a typo). Alternatively, you could do <code>subset(df, subset = age &gt;= 25)</code>."
        },
        {
        "owner": {
            "account_id": 8512965,
            "reputation": 15129,
            "user_id": 6382434,
            "user_type": "registered",
            "accept_rate": 75,
            "profile_image": "https://www.gravatar.com/avatar/8e1eef40e44288fb695dbdeb87aeb175?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "LMc",
            "link": "https://stackoverflow.com/users/6382434/lmc"
        },
        "edited": false,
        "score": 0,
        "creation_date": 1710536117,
        "post_id": 78169598,
        "comment_id": 137810172,
        "content_license": "CC BY-SA 4.0",
        "body": "Please read about <a href=\"https://stackoverflow.com/questions/5963269/how-to-make-a-great-r-reproducible-example\">how to make a great R reproducible example</a> and update your question accordingly. Include a sample of your data by pasting the output of <code>dput(&lt;your data frame&gt;)</code> into your post or <code>dput(head(&lt;your data frame&gt;))</code> if you have a large data frame. Also include code you have tried, any relevant errors, and expected output. If you cannot post your data, then post code for creating representative data. <a href=\"https://meta.stackoverflow.com/a/285557/6382434\">Do not post images of code and/or data</a>."
        }
    ]
    """)

answers_data = {
    "items": answers_response
}


comment_response = json.loads(r"""
    [
        {
        "owner": {
            "account_id": 8512965,
            "reputation": 15129,
            "user_id": 6382434,
            "user_type": "registered",
            "accept_rate": 75,
            "profile_image": "https://www.gravatar.com/avatar/8e1eef40e44288fb695dbdeb87aeb175?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "LMc",
            "link": "https://stackoverflow.com/users/6382434/lmc"
        },
        "edited": false,
        "score": 1,
        "creation_date": 1710536279,
        "post_id": 78169598,
        "comment_id": 137810186,
        "content_license": "CC BY-SA 4.0",
        "body": "This is pseudo code since you have not provided a reproducible example: <code>df[df$age &gt;=25,]</code> (the comma is not a typo). Alternatively, you could do <code>subset(df, subset = age &gt;= 25)</code>."
        },
        {
        "owner": {
            "account_id": 8512965,
            "reputation": 15129,
            "user_id": 6382434,
            "user_type": "registered",
            "accept_rate": 75,
            "profile_image": "https://www.gravatar.com/avatar/8e1eef40e44288fb695dbdeb87aeb175?s=256&d=identicon&r=PG&f=y&so-version=2",
            "display_name": "LMc",
            "link": "https://stackoverflow.com/users/6382434/lmc"
        },
        "edited": false,
        "score": 0,
        "creation_date": 1710536117,
        "post_id": 78169598,
        "comment_id": 137810172,
        "content_license": "CC BY-SA 4.0",
        "body": "Please read about <a href=\"https://stackoverflow.com/questions/5963269/how-to-make-a-great-r-reproducible-example\">how to make a great R reproducible example</a> and update your question accordingly. Include a sample of your data by pasting the output of <code>dput(&lt;your data frame&gt;)</code> into your post or <code>dput(head(&lt;your data frame&gt;))</code> if you have a large data frame. Also include code you have tried, any relevant errors, and expected output. If you cannot post your data, then post code for creating representative data. <a href=\"https://meta.stackoverflow.com/a/285557/6382434\">Do not post images of code and/or data</a>."
        }
    ]
    """)

comments_data = {
    "items": comment_response
}
