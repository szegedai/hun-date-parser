from spacy.language import Language
from spacy.tokens import Doc
from spacy.pipeline.sentencizer import Sentencizer
from spacy.pipeline import Pipe

from hun_date_parser import text2datetime


class HunDateParserComponent(Pipe):

    @staticmethod
    @Language.factory("hu_datetimes")
    def create_hu_datetime_component(nlp: Language, name: str, case_sensitive: bool):
        return HunDateParserComponent(nlp, case_sensitive)

    def __init__(self, nlp: Language, case_sensitive: bool):
        self.sentencizer = Sentencizer()

        if not Doc.has_extension("hu_datetimes"):
            Doc.set_extension("hu_datetimes", default=[])

    def __call__(self, doc: Doc) -> Doc:
        for sent in self.sentencizer(doc).sents:
            dt = text2datetime(sent.text)
            if dt:
                doc._.hu_datetimes.append(dt)
        return doc
