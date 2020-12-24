class Summoner:
    level = -1
    solo_rank = ""
    sub_rank = ""
    matchList = []

    def __init__(self, name):
        self.name = name

    def get_summoner_info(self, bs):
        self.__get_level(bs)
        self.__get_rank(bs)

    def get_match_list(self, bs):
        match_list = bs.select("div.Content > div.GameItemList > div.GameItemWrap")
        for match in match_list:
            winlose = match.select("div.GameResult")[0]
            champ_name = match.select("div.GameSettingInfo > div.ChampionName > a")[0]
            self.matchList.append({
                "Win": winlose.text.strip(),
                "ChampionName": champ_name.text.strip()
            })

    def msg_summoner_info(self):
        result = '{}\n' \
                 'level: {}\n' \
                 'solo rank: {} ({})\n' \
                 'sub rank: {} ({})' \
            .format(self.name,
                    self.level,
                    self.solo_rank["tier"],
                    self.solo_rank["point"],
                    self.sub_rank["tier"],
                    self.sub_rank["point"],
                    )
        return result

    def msg_match_list(self):
        result, count = "", 1
        for match in self.matchList:
            result += str(count) + ' : ' \
                      + str(match["ChampionName"]) + ' ' \
                      + str("승리" if match["Win"] == "Victory" else "패배") \
                      + '\n'
            count += 1
        self.matchList.clear()
        return result

    def __get_level(self, bs):
        user_level = bs.select("div.ProfileIcon > span.Level")[0]
        self.level = user_level.text.strip()

    def __get_rank(self, bs):
        self.__get_solo_rank(bs)
        self.__get_sub_rank(bs)

    def __get_solo_rank(self, bs):
        try:
            tier = bs.select("div.TierRank")[0]
            point = bs.select("div.TierInfo > span.LeaguePoints")[0]
            self.solo_rank = {
                "tier": tier.text.strip(),
                "point": point.text.strip()
            }
        except:
            self.solo_rank = {
                "tier": "Unranked",
                "point": "0LP"
            }

    def __get_sub_rank(self, bs):
        try:
            tier = bs.select("div.sub-tier__rank-tier")[0]
            point = bs.select("div.sub-tier__info > div.sub-tier__league-point")[0]
            if point.select('.sub-tier__gray-text') is not None:
                point.select_one('.sub-tier__gray-text').decompose()
            self.sub_rank = {
                "tier": tier.text.strip(),
                "point": point.text.strip()
            }
        except:
            self.sub_rank = {
                "tier": "Unranked",
                "point": "0LP"
            }