from flask import Flask

from App.Controllers.ScrapeController import ScrapeController

app = Flask(__name__)

scrapeController = ScrapeController()


app.add_url_rule('/', view_func=scrapeController.run)

if __name__ == "__main__":
    app.run(debug=True)
