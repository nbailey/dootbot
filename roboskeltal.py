# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 22:15:46 2015

@author: Nate
"""

import praw
import random
import time

from datetime import datetime
from templates import *


user_agent = 'LeDootGeneration_SS reposter bot 1.0 by /u/slate15'

print 'Starting RoboSkeltal! Doot doot.'

print 'Signing in...'

r = praw.Reddit(user_agent=user_agent)
r.login('roboskeltal', 'CALc1um')

print 'Signed in!'

user_name = 'ledootgeneration_ss'
user = r.get_redditor(user_name)

submission_ids = [s.id for s in user.get_submitted(limit=None)]
comment_ids = [c.id for c in user.get_comments(limit=None)]

print 'Setup complete\n'

while True:
    # Get recent submissions
    print 'Finding submissions...'
    submissions = user.get_submitted(limit=5)

    # Repost new submissions to /r/ledootgeneration
    for submission in submissions:
        if submission.id not in submission_ids:
            print 'New submission found!'

            title = submission.title
            # Copy self text for self posts
            if submission.is_self:
                selftext = submission.selftext
                s = r.submit('ledootgeneration', title=title, text=selftext)
            # Copy url for link posts
            else:
                url = submission.url
                s = r.submit('ledootgeneration', title=title, url=url)

            print 'Submitted to /r/ledootgeneration: {}'.format(s.permalink)

            # Post to /r/roboskeltal linking to original and copy
            dt = datetime.fromtimestamp(s.created_utc)
            orig = submission.permalink
            xpost = s.permalink
            s2 = r.submit('roboskeltal', title=title,
                          text=submission_template.format(dt, orig, xpost))

            print 'Submitted to /r/roboskeltal: {}'.format(s2.permalink)

            # Add to list of submission ids
            submission_ids.append(submission.id)

    # Get recent comments
    print 'Finding comments...'
    comments = user.get_comments(limit=5)

    # Repost new comments on rising /r/ledootgeneration posts
    for comment in comments:
        if comment.id not in comment_ids:
            print 'New comment found!'

            # Find a /r/ledootgeneration post to comment on
            doot = r.get_subreddit('ledootgeneration')
            rising = list(doot.get_rising())
            if not rising:
                hot = list(doot.get_hot(limit=3))
                thread = random.choice(hot)
            else:
                thread = random.choice(rising)

            c = thread.add_comment(comment.body)
            print 'Commented on /r/ledootgeneration: {}'.format(c.permalink)

            # Post to /r/roboskeltal linking to original and copy
            dt = datetime.fromtimestamp(c.created_utc)
            orig = comment.permalink
            xpost = c.permalink
            title = (comment.body[:297] + '...') if len(comment.body)>300 else comment.body
            s = r.submit('roboskeltal', title=title,
                     text=comment_template.format(dt, orig, xpost))

            print 'Submitted to /r/roboskeltal: {}'.format(s.permalink)

            # Add to list of comment ids
            comment_ids.append(comment.id)

    print 'Sleeping... sweet dreams of calcium and updoots'
    time.sleep(1800)
