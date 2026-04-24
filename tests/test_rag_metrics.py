from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)
from src.config import LLM_MODEL
from src.database import search_filmes
from src.llm import ask

_QUERY = "Indique filmes brasileiros aclamados pela crítica"
_EXPECTED = "Cidade de Deus e Central do Brasil são exemplos de filmes brasileiros muito aclamados."


def test_rag_metrics(judge, db):
    ctx = search_filmes(db, _QUERY)
    actual_output = ask(LLM_MODEL, _QUERY, ctx)

    test_case = LLMTestCase(
        input=_QUERY,
        actual_output=actual_output,
        expected_output=_EXPECTED,
        retrieval_context=ctx,
    )

    assert_test(test_case, [
        FaithfulnessMetric(threshold=0.5, model=judge),
        ContextualPrecisionMetric(threshold=0.4, model=judge),
        ContextualRecallMetric(threshold=0.4, model=judge),
        ContextualRelevancyMetric(threshold=0.5, model=judge),
    ])
