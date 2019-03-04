""" Usage:
    analyze --in=INPUT_FILE --out=OUTPUT_FILE

    Analyze question distribution in QA-SRL input file. Store the output in the given output file.
"""
from collections import defaultdict
from docopt import docopt
import logging
logging.basicConfig(level = logging.DEBUG)
from nltk.stem import WordNetLemmatizer

from oie_readers.extraction import QUESTION_OBJ2_INDEX, QUESTION_PP_INDEX, QUESTION_TRG_INDEX,\
    generalize_question

from read_data import QASRL_extractor

class Analyzer:
    """
    Container for analysis functions
    """
    def __init__(self):
        """
        Intialize memebers:
        question_dist - generalized-question distribution of the assigned extraction
                        location.
        """
        self.question_dist = defaultdict(lambda : defaultdict(lambda : 0))
        self.lmtzr = WordNetLemmatizer()

    def analyze_question_patterns(self, extractions):
        """
        Calcualtes a per generalized-question distribution of the assigned location in
        the tuple. Stores the output in the question_distribution memeber variable.
        """
        for ex in extractions:
            # Count the observed location for each generalized question
            for ind, gen_question in enumerate([generalize_question(question)
                                                for (_, question) in ex.getSortedArgs()]):
                self.question_dist[gen_question][ind] += 1

    def get_dist(self):
        """
        Get simple dict representation of the distribtion
        """
        return dict([(k, v)
                     for k, v in self.question_dist.items()])

    def get_sorted_dist(self):
        """
        Get the question distribution sorted by occurences
        """
        return sorted(iter(self.get_dist().items()),
                      key = lambda q_dist: sum(q_dist[1].values()),
                      reverse = True)

    def output_dist_to_file(self, json_fn):
        """
        Write this distribution (as a sorted list, based on occurences)
        to an output json file
        """
        import json
        with open(json_fn, 'w') as fout:
            json.dump(self.get_dist(),
                      fout)


if __name__ == "__main__":
    # Parse arguments
    #args = docopt(__doc__)
    #logging.debug(args)
    #fin = args['--in']
    #fout = args['--out']
    qa_path = 'test.jsonl'
    dist_file = ''
    output_file = 'q_dist_test.json'
    write = False
    min_correct = 5/6
    QASRL_extractor = QASRL_extractor(qa_path, output_file, dist_file, write, min_correct)
    QASRL_extractor.read()



    # Get extractions
    #logging.info("Reading QA-SRL from: {}".format(fin))
    #q = Qa2OIE(fin)
    extractions = QASRL_extractor.extractions

    # Analyze frequency
    #logging.info("Analyzing frquency")
    analyzer = Analyzer()
    analyzer.analyze_question_patterns(extractions)
    d = analyzer.get_sorted_dist()

    # Write to file
    #logging.info("Writing output to file: {}".format(fout))
    analyzer.output_dist_to_file(output_file)

    #logging.info("DONE!")
