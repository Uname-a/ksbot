FROM python:3

RUN pip install praw
CMD [ "python", "/ksbot/monthly_trade_post.py" ]

