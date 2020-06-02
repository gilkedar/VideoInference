
from Utils.Settings import Config

class IsSantaResponse():

    field_santa_prob = "santa_prob"
    field_not_santa_prob = "not_santa_prob"
    field_is_santa_ans = "is_santa_ans"

    def __init__(self, is_santa_ans,santa_prob,not_santa_prob):
        self.is_santa_ans = is_santa_ans
        self.santa_prob = santa_prob
        self.not_santa_prob = not_santa_prob

    def serialize(self):
        dic = dict()
        dic[self.field_is_santa_ans] = self.is_santa_ans
        dic[self.field_santa_prob] = str(self.santa_prob)
        dic[self.field_not_santa_prob] = str(self.not_santa_prob)
        return dic

    @staticmethod
    def getLabel( response_dic):
        santa = float(response_dic[IsSantaResponse.field_santa_prob])
        notSanta = float(response_dic[IsSantaResponse.field_not_santa_prob])
        label = "Santa" if santa > notSanta else "Not Santa"
        proba = santa if santa > notSanta else notSanta
        label = "{}: {:.5f}%".format( label, proba * 100)
        return label

