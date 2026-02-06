from enrichment import enrichment_curve, screening_savings


def test_enrichment_curve_expected_rates():
    y_true = [1] * 50 + [0] * 50
    y_score = list(reversed(range(100)))
    curve, base_rate = enrichment_curve(y_true, y_score, percentiles=[10, 20, 50])
    assert base_rate == 0.5
    assert curve.loc[curve["percentile"] == 10, "yield_rate"].iloc[0] == 1.0
    assert curve.loc[curve["percentile"] == 50, "yield_rate"].iloc[0] == 1.0


def test_screening_savings_reduction():
    base_needed, enriched_needed, reduction = screening_savings(0.1, 0.2, target_n=100)
    assert base_needed == 1000
    assert enriched_needed == 500
    assert reduction == 0.5
