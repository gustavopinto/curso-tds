from tabnanny import verbose
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from src.config import LLM_MODEL
from src.llm import ask

input = "Quero um filme emocionante para assistir hoje à noite"

test_case = LLMTestCase(
    input=input,
    actual_output=ask(LLM_MODEL, input),
    expected_output="Uma boa recomendação de filme emocionante."
)


def test_base(judge):
    assert_test(test_case, 
        [AnswerRelevancyMetric(threshold=0.5, model=judge, verbose_mode=True)]
    )


