@classmethod
    def _slice(cls, input_dict_list):
        slice_num = 100
        length = len(input_dict_list)
        temp_list = list()
        for i in range(0, length, slice_num):
            temp_list.append(input_dict_list[i:i + slice_num])
        return temp_list
