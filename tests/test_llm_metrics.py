from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import AnswerRelevancyMetric, BiasMetric, GEval, ToxicityMetric
from src.config import LLM_MODEL
from src.llm import ask

_QUERY = "Quero assistir um filme de ação cheio de adrenalina"
_EXPECTED = "Filmes de ação como Duro de Matar e Mad Max são ótimas opções."


def test_llm_metrics(judge):
    test_case = LLMTestCase(
        input=_QUERY,
        actual_output=ask(LLM_MODEL, _QUERY),
        expected_output=_EXPECTED,
    )

    assert_test(test_case, [
        GEval(
            name="Correctness",
            criteria="A resposta recomenda filmes coerentes com o pedido do usuário.",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.4,
            model=judge,
            verbose_mode=True
        ),
        GEval(
            name="Conciseness",
            criteria="A resposta é concisa e objetiva, sem informações desnecessárias.",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.4,
            model=judge,
            verbose_mode=True
        ),
        AnswerRelevancyMetric(threshold=0.5, model=judge, verbose_mode=True),
        ToxicityMetric(threshold=0.5, model=judge, verbose_mode=True),
        BiasMetric(threshold=0.5, model=judge, verbose_mode=True),
    ])
