"""
Unit tests для анализа DBpedia.
"""

import unittest
from typing import Dict, List

from assignment import load_dbpedia_dataset, analyze_category_distribution
from dbpedia_modules import (
    preprocess_text,
    get_category_name,
    analyze_text_statistics,
    extract_top_words_by_category,
)


class TestDBpediaAnalysis(unittest.TestCase):
    """Тесты для анализа датасета DBpedia."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.sample_dataset = [
            {
                "title": "Test Company",
                "content": "This is a test company that produces software products.",
                "label": 0,
            },
            {
                "title": "Test University",
                "content": "A educational institution offering degrees in computer science.",
                "label": 1,
            },
            {
                "title": "Test Artist",
                "content": "Famous painter known for landscape artworks and exhibitions.",
                "label": 2,
            },
        ]

    def test_preprocess_text_functionality(self) -> None:
        """Тест: функция предобработки текста работает корректно."""
        text = "The quick brown fox jumps over the lazy dog!"
        result = preprocess_text(text)
        expected = ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        self.assertEqual(result, expected)

    def test_get_category_name_range(self) -> None:
        """Тест: получение имен категорий для всех 14 labels."""
        for label in range(14):
            category_name = get_category_name(label)
            self.assertIsInstance(category_name, str)
            self.assertTrue(len(category_name) > 0)

    def test_analyze_category_distribution_counts(self) -> None:
        """Тест: подсчет распределения по категориям."""
        result = analyze_category_distribution(self.sample_dataset)

        # Проверяем правильность подсчета
        self.assertEqual(result["Company"], 1)
        self.assertEqual(result["EducationalInstitution"], 1)
        self.assertEqual(result["Artist"], 1)

        # Проверяем общее количество
        total_count = sum(result.values())
        self.assertEqual(total_count, len(self.sample_dataset))

    def test_analyze_text_statistics_structure(self) -> None:
        """Тест: структура возвращаемой статистики текстов."""
        result = analyze_text_statistics(self.sample_dataset)

        # Проверяем наличие всех ожидаемых ключей
        self.assertIn("title", result)
        self.assertIn("content", result)

        # Проверяем базовые метрики
        title_stats = result["title"]
        expected_metrics = [
            "mean_length",
            "median_length",
            "min_length",
            "max_length",
            "std_length",
        ]
        for metric in expected_metrics:
            self.assertIn(metric, title_stats)
            self.assertIsInstance(title_stats[metric], float)

    def test_extract_top_words_structure(self) -> None:
        """Тест: структура возвращаемых топ слов."""
        result = extract_top_words_by_category(self.sample_dataset, top_n=25)

        # Проверяем наличие категорий
        expected_categories = ["Company", "EducationalInstitution", "Artist"]
        for category in expected_categories:
            self.assertIn(category, result)

            # Проверяем формат данных
            top_words = result[category]
            self.assertIsInstance(top_words, list)
            if top_words:
                self.assertIsInstance(top_words[0], tuple)
                self.assertEqual(len(top_words[0]), 2)

    def test_text_statistics_values_validity(self) -> None:
        """Тест: валидность значений статистики текстов."""
        stats = analyze_text_statistics(self.sample_dataset)

        # Проверяем логику значений
        title_stats = stats["title"]
        self.assertLessEqual(title_stats["min_length"], title_stats["median_length"])
        self.assertLessEqual(title_stats["median_length"], title_stats["max_length"])

        # Проверяем неотрицательность
        for metric in title_stats.values():
            self.assertGreaterEqual(metric, 0)


if __name__ == "__main__":
    unittest.main()
