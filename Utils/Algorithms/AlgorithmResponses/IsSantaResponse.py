
from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage
from Utils.Settings import Config

class IsSantaResponseMessage():

    field_santa_prob = "santa_prob"
    field_not_santa_prob = "not_santa_prob"
    field_is_santa_ans = "is_santa_ans"

    def __init__(self, is_santa_ans,santa_prob,not_santa_prob):
        self.is_santa_ans = is_santa_ans
        self.santa_prob = santa_prob
        self.not_santa_prob = not_santa_prob

    def serialize(self):
        dic = dict()
        dic[self.is_santa_ans] = self.is_santa_ans
        dic[self.field_santa_prob] = "{:.3f}".format(self.santa_prob)
        dic[self.field_not_santa_prob] = "{:.3f}".format(self.not_santa_prob)
        return dic
