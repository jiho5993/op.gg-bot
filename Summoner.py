class Summoner:
    level = ""
    solo_rank = ""
    sub_rank = ""

    def __init__(self, name):
        self.name = name

    def get_level(self, bs):
        user_level = bs.select("div.ProfileIcon > span.Level")[0]
        self.level = user_level.text.strip()

    def get_solo_rank(self, bs):
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

    def get_sub_rank(self, bs):
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

    def get_rank(self, bs):
        self.get_solo_rank(bs)
        self.get_sub_rank(bs)