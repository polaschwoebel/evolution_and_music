def transcribe_input(input_string):
    score = 0
    for i in input_string:
        if i == '-':
            score -= 1
        if i == '+' or i == '=':
            score += 1
    return score
