class MergeDict:
    def __init__(self):
        self

    @staticmethod
    def merge_dicts(dict1, dict2):
        """
        function to merge dictionaries together

        :param dict1:
        :param dict2:
        :return:
        """

        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = [value, dict1[key]]
        return dict3
