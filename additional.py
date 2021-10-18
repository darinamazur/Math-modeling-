class Additional:

    def clean_list(self, lst):
        res = []
        for x in lst:
            res.insert(0,','.join(x))
        return res