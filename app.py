from flask import Flask

from App.Controllers.ScrapeController import ScrapeController

app = Flask(__name__)

scrapeController = ScrapeController()


app.add_url_rule('/', view_func=scrapeController.run)
app.add_url_rule('/update/<username>', view_func=scrapeController.scrape_by_username)

if __name__ == "__main__":
    app.run(debug=True)
