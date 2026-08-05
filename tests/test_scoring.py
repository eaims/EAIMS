import copy
import unittest

from eaims.scoring import AssessmentError, score_assessment, validate_assessment


def assessment(score=3, confidence="high"):
    return {
        "standard": "EAIMS", "version": "0.2.0", "organization": "Test Org",
        "assessment_date": "2026-08-03", "assessment_type": "self", "scope": "Enterprise",
        "capability_scores": [
            {"capability_id": f"{d}.{c}", "score": score, "confidence": confidence,
             "evidence_ids": [f"EV-{d}{c}"] if score >= 3 else []}
            for d in range(1, 10) for c in range(1, 4)
        ],
    }


class ScoringTests(unittest.TestCase):
    def test_level_three(self):
        result = score_assessment(assessment())
        self.assertEqual(result["final_level"], 3)
        self.assertEqual(result["aggregate_score"], 3)

    def test_critical_gate_caps_level(self):
        data = assessment(4)
        for row in data["capability_scores"]:
            if row["capability_id"].startswith("7."):
                row["score"] = 1
                row["evidence_ids"] = []
        result = score_assessment(data)
        self.assertEqual(result["final_level"], 3)
        self.assertTrue(result["gate_adjustments"])

    def test_level_five_requires_every_dimension_at_four(self):
        data = assessment(5)
        for row in data["capability_scores"]:
            if row["capability_id"].startswith("2."):
                row["score"] = 3
        self.assertEqual(score_assessment(data)["final_level"], 4)

    def test_low_confidence_is_provisional(self):
        self.assertTrue(score_assessment(assessment(confidence="low"))["provisional"])

    def test_missing_capability_rejected(self):
        data = assessment()
        data["capability_scores"].pop()
        self.assertIn("missing capabilities", " ".join(validate_assessment(data)))

    def test_duplicate_rejected(self):
        data = assessment()
        data["capability_scores"].append(copy.deepcopy(data["capability_scores"][0]))
        self.assertIn("duplicate", " ".join(validate_assessment(data)))

    def test_level_three_requires_evidence(self):
        data = assessment()
        data["capability_scores"][0]["evidence_ids"] = []
        self.assertIn("requires", " ".join(validate_assessment(data)))

    def test_exclusion_requires_rationale(self):
        data = assessment()
        data["capability_scores"][0] = {"capability_id": "1.1", "not_applicable": True}
        self.assertIn("rationale", " ".join(validate_assessment(data)))

    def test_invalid_input_cannot_score(self):
        with self.assertRaises(AssessmentError):
            score_assessment({})


if __name__ == "__main__":
    unittest.main()
