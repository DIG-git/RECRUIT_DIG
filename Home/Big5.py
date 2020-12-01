class Big5():
    def __init__(self):
        self.questions_key = {
            'I am the life of the party.': 'E1',
            "I don't talk a lot.": 'E2',
            'I feel comfortable around people.': 'E3',
            'I keep in the background.': 'E4',
            'I start conversations.': 'E5',
            'I have little to say.': 'E6',
            'I talk to a lot of different people at parties.': 'E7',
            "I don't like to draw attention to myself.": 'E8',
            "I don't mind being the center of attention.": 'E9',
            'I am quiet around strangers.': 'E10',
            'I get stressed out easily.': 'N1',
            'I am relaxed most of the time.': 'N2',
            'I worry about things.': 'N3',
            'I seldom feel blue.': 'N4',
            'I am easily disturbed.': 'N5',
            'I get upset easily.': 'N6',
            'I change my mood a lot.': 'N7',
            'I have frequent mood swings.': 'N8',
            'I get irritated easily.': 'N9',
            'I often feel blue.': 'N10',
            'I feel little concern for others.': 'A1',
            'I am interested in people.': 'A2',
            'I insult people.': 'A3',
            "I sympathize with others' feelings.": 'A4',
            "I am not interested in other people's problems.": 'A5',
            'I have a soft heart.': 'A6',
            'I am not really interested in others.': 'A7',
            'I take time out for others.': 'A8',
            "I feel others' emotions.": 'A9',
            'I make people feel at ease.': 'A10',
            'I am always prepared.': 'C1',
            'I leave my belongings around.': 'C2',
            'I pay attention to details.': 'C3',
            'I make a mess of things.': 'C4',
            'I get chores done right away.': 'C5',
            'I often forget to put things back in their proper place.': 'C6',
            'I like order.': 'C7',
            'I shirk my duties.': 'C8',
            'I follow a schedule.': 'C9',
            'I am exacting in my work.': 'C10',
            'I have a rich vocabulary.': 'O1',
            'I have difficulty understanding abstract ideas.': 'O2',
            'I have a vivid imagination.': 'O3',
            'I am not interested in abstract ideas.': 'O4',
            'I have excellent ideas.': 'O5',
            'I do not have a good imagination.': 'O6',
            'I am quick to understand things.': 'O7',
            'I use difficult words.': 'O8',
            'I spend time reflecting on things.': 'O9',
            'I am full of ideas.': 'O10',
        }
        self.negative_keyed = [
            "I don't talk a lot.",
            'I keep in the background.',
            'I have little to say.',
            "I don't like to draw attention to myself.",
            'I am quiet around strangers.',
            'I am relaxed most of the time.',
            'I seldom feel blue.',
            'I feel little concern for others.',
            'I insult people.',
            "I am not interested in other people's problems.",
            'I am not really interested in others.',
            'I leave my belongings around.',
            'I make a mess of things.',
            'I often forget to put things back in their proper place.',
            'I shirk my duties.',
            'I am exacting in my work.',
            'I have difficulty understanding abstract ideas.',
            'I am not interested in abstract ideas.',
            'I do not have a good imagination.']

    def handle_personality_test(self, answers):
        answer_dict = {}
        for question, answer in answers.items():
            if question in self.negative_keyed:
                answer = 6 - answer
            key = self.questions_key[question]
            answer_dict[key] = answer

        score_dict = {'O_score': 0, 'C_score': 0, 'E_score': 0, 'A_score': 0, 'N_score': 0}
        for trait_key, answer in answer_dict.items():
            if 'O' in trait_key:
                score_dict['O_score'] += answer
            if 'C' in trait_key:
                score_dict['C_score'] += answer
            if 'E' in trait_key:
                score_dict['E_score'] += answer
            if 'A' in trait_key:
                score_dict['A_score'] += answer
            if 'N' in trait_key:
                score_dict['N_score'] += answer

        for key, score in score_dict.items():
            score_dict[key] = score / 10

        perc_dict = {}
        for key, score in score_dict.items():
            perc = (score / 5) * 100
            perc_dict[key] = round(perc)

        return (perc_dict)
