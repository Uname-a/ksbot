FROM python:3
ADD monthly_trade_post.py /

RUN pip install praw
CMD [ "python", "./monthly_trade_post.py" ]

