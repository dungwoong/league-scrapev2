import requests
import random

import RequestSender
import time
import APICollector
import CustomExceptions
import Logger
import WebScrapeCollector
import RoleIdentifier


def enter_api_keys():
    RequestSender.add_keys(["RGAPI-6ec2c68c-5e1d-4ffa-821b-4af77abd8231"])


def test_requests():
    enter_api_keys()

    codes = dict()

    def add_code(code, cdodes):
        if code not in cdodes:
            cdodes[code] = 1
        else:
            cdodes[code] += 1

    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/PlatypusOfCanada?api_key=<API_KEY>"

    start_time = int(time.time())
    count = 0
    while int(time.time()) < (start_time + 120):
        count += 1
        resp = RequestSender.send_request(url)
        add_code(resp.status_code, codes)
        print("count=" + str(count), ", code=" + str(resp.status_code))

    print("sent " + str(count) + " requests in " + str(int(time.time()) - start_time) + " seconds.")
    print(codes)


def test_process_url():
    assert RequestSender.process_url("www.google.ca/<A>/<B><C>", {"A": "hello", "B": "MY", "C": "man"}) == \
           "www.google.ca/hello/MYman"


def test_summoner_v4(name):
    Logger.VERBOSITY_LEVEL = "ALL"
    try:
        player = APICollector.BasicSummonerInfo(name)
        print(player.info)
        ranked_info = APICollector.SummonerRankedInfo(player)
        print(ranked_info["rank"], ranked_info["tier"], ranked_info["lp"])
        matches = APICollector.SummonerGameBuffer(player)
        match = matches.matches[0]
        game = APICollector.HistoryLeagueGame(match, player)
        print("time: " + str(game.game_time))
        print("winning team:", game.winning_team)
        print("team kills:", game.team_kills)
        print("individual data:", game.individual_data)
    except CustomExceptions.APICallException as e:
        print(e)


def test_get_log(name):
    try:
        soup = WebScrapeCollector.get_response(name, WebScrapeCollector.LOG_URL_CHAMPIONS)
        with open("output2.html", "wb") as file:
            file.write(soup.prettify("utf-8"))
    except Exception as e:
        print(e)


def test_get_infos(name):
    try:
        soup = WebScrapeCollector.get_response(name, WebScrapeCollector.LOG_URL_1)

        print(WebScrapeCollector.find_role_wr(soup, "Jungler"))
    except Exception as e:
        print(e)


def test_get_champ_infos(name):
    try:
        soup = WebScrapeCollector.get_response(name, WebScrapeCollector.LOG_URL_CHAMPIONS)
        champ_dict = WebScrapeCollector.get_champ_datas(soup)
        for key in champ_dict:
            print(key, champ_dict[key])
    except Exception as e:
        print(e)


def test_get_champ_infos(name, champion_name):
    soup = WebScrapeCollector.get_response(name, WebScrapeCollector.LOG_URL_CHAMPIONS)
    print(WebScrapeCollector.get_champ_wr_played(soup, champion_name))


def test_champ_compare_score():
    champ1 = input("champ input: ")
    champ2 = input("champ to compare to(on LOG): ")
    print(WebScrapeCollector.get_name_match_score(champ1, champ2))


def test_champ_compare_score2():
    jason = requests.get("http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json")
    champ_data = jason.json()["data"]
    random1 = random.randint(0, len(champ_data) - 1)
    random2 = random.randint(0, len(champ_data) - 1)
    champ1 = list(champ_data.keys())[random1]
    champ2 = list(champ_data.keys())[random2]
    score = WebScrapeCollector.get_name_match_score(champ1, champ2)
    if score > 0.99:
        Logger.message(champ1 + " equals " + champ2)
    elif score > 0.5:
        Logger.warning(champ1 + " match score " + str(score) + " with " + champ2)
    elif score > 0:
        Logger.alert(champ1 + " match score " + str(score) + " with " + champ2)
    else:
        pass


def get_some_games(sumname):
    bsi = APICollector.BasicSummonerInfo(sumname)
    games = APICollector.SummonerGameBuffer(bsi)
    print(games.matches)


def test_get_roles(matchid):
    all_json = APICollector.get_game_data(matchid)[0]
    all_json = APICollector.get_rgapi_json(all_json)
    position_dict = APICollector.get_team_names_and_positions(all_json)
    for team in position_dict:
        print(team, "\n")
        print(position_dict[team])


enter_api_keys()
# test_summoner_v4("PlatypusOfCanada")
# test_summoner_v4("waste it on me")

test_get_champ_infos("waste it on me", "Lee Sin")
# test_get_champ_infos("Sudden Stirke", "master yi")
games = ['NA1_4152493334', 'NA1_4144890019', 'NA1_4144645173', 'NA1_4144616999', 'NA1_4144601202', 'NA1_4142425411', 'NA1_4142319290', 'NA1_4142276540', 'NA1_4142225392', 'NA1_4142220426']
# get_some_games("waste it on me")
# test_get_roles('NA1_4144890019')
