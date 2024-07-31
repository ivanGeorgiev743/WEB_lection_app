from flask import Flask, request, jsonify
from functionalities import *
from sqlalchemy import create_engine
from models import *
from Config import config
from sqlalchemy.dialects.mysql import insert

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route("/sum", methods=["GET", "POST"])
def sum_page():
    try:
        return {
            "response": sum_numbers(
                *[request.args[k] for k in request.args if "num" in k]
            )
        }
    except Exception as ex:
        return {"error": str(ex)}, 500


@app.route("/pow")
def pow_page():
    try:
        return {"response": pow_numbers(*request.args.values())}
    except Exception as ex:
        return {"error": str(ex)}, 500


@app.route("/prices", methods=["GET", "POST"])
def prices():
    return jsonify(get_prices(request.args["ticker"]))


@app.route("/upload_prices", methods=["GET", "POST"])
def upload_prices():
    ticker = request.args["ticker"]
    prices_data = get_prices(ticker)
    with Session(engine) as session:
        for price in prices_data:
            entry = HistModel(date=price["Date"], close=price["Close"], ticker=ticker.upper())
            existing_entry = session.query(HistModel).filter_by(date=price["Date"], ticker=ticker.upper()).first()
            if existing_entry:
                existing_entry.close = price["Close"]
            else:
                session.add(entry)
        session.commit()
    #    upload_via_pandas(ticker, engine)
    return {"status": "OK"}, 200


if __name__ == "__main__":
    engine = create_engine(config("conn_str"), echo=True)
    Base.metadata.create_all(engine)
    app.run()
