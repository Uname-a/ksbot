FROM python:3
ADD my_script.py /

RUN pip install praw
CMD [ "python", "./monthly_trade_post.py" ]

