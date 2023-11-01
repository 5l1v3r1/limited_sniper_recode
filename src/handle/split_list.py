def get(input_list: list, max_len: int = 120):
    if len(input_list) <= 120:
        return [input_list]
        
    input_list *= -(-max_len // len(input_list))
    return [input_list[i:i+max_len] for i in range(0, len(input_list), max_len)]