from flask import Flask, jsonify
from thesportsdb import leagues

app = Flask(__name__)


@app.route('/')
def hello_world():

    league_table = leagues.leagueSeasonTable('4328', '2020-2021')

    for key, value in league_table.items():
        for k in value:
            print(k['strTeam'], ' : ', k['strLeague'], ' : ', k['strForm'])

    return league_table


if __name__ == '__main__':
    app.run()
