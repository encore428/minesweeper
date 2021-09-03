## To execute (on Windows)

Open an Anaconda Prompt session, perform the following:

```
git clone https://github.com/encore428/minesweeper
cd Python/minesweeper
source venv/Scripts/activate
flask run
```

## Architecture

**Api**

Blueprints of the api of the game:

- init game
- update game

**Minesweeper**

### Software architecture

![software architecture](/software-architecture.jpg)

### User flow

![user flow](/user-flow.jpg)

### External game API

![external api](/external-api-design.jpg)

### UML diagram

![uml diagram](/uml.jpg)

**Pages**

Blueprints of the pages on frontend. We will store the static and templates here for it to be self-contained as a front-end only folder.

## Resources

[Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)

[Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/)

[Flask realworld example app](https://github.com/gothinkster/flask-realworld-example-app)

## Notes

When Developing, always make sure to run on dev mode via environment variable `export FLASK_DEBUG=True`
