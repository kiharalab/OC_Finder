

def Load_CPU_Model(state_dict,model):
    """

    :param state_dict: default gpu saved model
    :param model: we want it to be a cpu model
    :return:
    """

    pretrained_dict = {}
    for key in state_dict.keys():
        param=state_dict[key]
        param=param.cpu()
        new_key=key[7:]
        pretrained_dict[new_key]=param
        print("CPU version specified key:"+new_key)
    model.load_state_dict(pretrained_dict)
    return model