# Stack Exchange Best Questions

Simple "almost"-no-code bot, that posts most viewed questions from stack exchange boards.

Architecture:
    - sanic server
        - parse se website
        - keeps track of sent messages
    - integromat
        - pings the server every 1.5 hours for new questions
        - sends question to telegram chanel