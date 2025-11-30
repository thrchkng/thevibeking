"""
Модуль с вспомогательными функциями для анализа DBpedia.
"""

import re
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Словарь категорий DBpedia
CATEGORY_NAMES = {
    0: "Company",
    1: "EducationalInstitution",
    2: "Artist",
    3: "Athlete",
    4: "OfficeHolder",
    5: "MeanOfTransportation",
    6: "Building",
    7: "NaturalPlace",
    8: "Village",
    9: "Animal",
    10: "Plant",
    11: "Album",
    12: "Film",
    13: "WrittenWork",
}


def preprocess_text(text: str) -> List[str]:
    """
    Предобрабатывает текст: токенизация, приведение к нижнему регистру, удаление стоп-слов.

    Args:
        text: Исходный текст.

    Returns:
        List[str]: Список токенов после предобработки.
    """
    if not text:
        return []

    # Приведение к нижнему регистру
    text = text.lower()

    # Удаление специальных символов и цифр, оставляем только буквы
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Токенизация по пробелам
    tokens = text.split()

    # Базовый список стоп-слов для английского языка
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "they",
        "them",
        "their",
        "he",
        "she",
        "his",
        "her",
        "him",
        "we",
        "our",
        "us",
        "you",
        "your",
        "i",
        "me",
        "my",
        "mine",
        "from",
        "as",
        "so",
        "than",
        "too",
        "very",
        "has",
        "have",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "can",
        "shall",
    }

    # Фильтрация стоп-слов и коротких слов
    filtered_tokens = [
        token for token in tokens if token not in stop_words and len(token) > 2
    ]

    return filtered_tokens


def get_category_name(label: int) -> str:
    """
    Возвращает название категории для числового label.

    Args:
        label: Числовой идентификатор категории (0-13).

    Returns:
        str: Название категории.
    """
    return CATEGORY_NAMES[label]


def analyze_text_statistics(
    dataset: List[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    """
    Анализирует статистику заголовков и контента.

    Args:
        dataset: Список примеров с полями 'title' и 'content'.

    Returns:
        Dict: Статистика для title и content.
    """
    # Используем pandas для эффективного анализа
    df = pd.DataFrame(dataset)

    # Анализ длины в символах
    title_lengths = df["title"].str.len().values
    content_lengths = df["content"].str.len().values

    # Анализ длины в словах с использованием preprocess_text
    title_word_counts = np.array([len(preprocess_text(title)) for title in df["title"]])
    content_word_counts = np.array(
        [len(preprocess_text(content)) for content in df["content"]]
    )

    def calculate_stats(
        lengths: np.ndarray, word_counts: np.ndarray
    ) -> Dict[str, float]:
        """Вычисляет расширенную статистику."""
        # Используем numpy для вычисления статистики
        percentiles = np.percentile(lengths, [25, 50, 75, 90])

        return {
            "mean_length": float(np.mean(lengths)),
            "median_length": float(np.median(lengths)),
            "min_length": float(np.min(lengths)),
            "max_length": float(np.max(lengths)),
            "std_length": float(np.std(lengths)),
            "q1_length": float(percentiles[0]),
            "q3_length": float(percentiles[2]),
            "p90_length": float(percentiles[3]),
            "mean_word_count": float(np.mean(word_counts)),
            "median_word_count": float(np.median(word_counts)),
            "vocabulary_richness": float(np.mean(word_counts) / np.mean(lengths))
            if np.mean(lengths) > 0
            else 0.0,
        }

    return {
        "title": calculate_stats(title_lengths, title_word_counts),
        "content": calculate_stats(content_lengths, content_word_counts),
    }


def extract_top_words_by_category(
    dataset: List[Dict[str, Any]], top_n: int = 25
) -> Dict[str, List[Tuple[str, int]]]:
    """
    Извлекает топ-N слов для каждой категории.

    Args:
        dataset: Список примеров с полями 'content' и 'label'.
        top_n: Количество топовых слов для извлечения.

    Returns:
        Dict: Топ слова по категориям {category: [(word, frequency), ...]}.
    """
    category_words = defaultdict(list)

    # Используем pandas для группировки по категориям
    df = pd.DataFrame(dataset)

    for label in range(14):
        category_name = get_category_name(label)
        # Фильтруем данные по категории
        category_data = df[df["label"] == label]

        # Обрабатываем все тексты категории
        all_tokens = []
        for content in category_data["content"]:
            tokens = preprocess_text(content)
            all_tokens.extend(tokens)

        category_words[category_name] = all_tokens

    # Подсчитываем частоты и извлекаем топ-N с использованием Counter
    top_words_by_category = {}
    for category, words in category_words.items():
        word_freq = Counter(words)
        top_words_by_category[category] = word_freq.most_common(top_n)

    return top_words_by_category


def create_visualization(category_distribution: Dict[str, int]) -> None:
    """
    Создает horizontal bar chart распределения по категориям.

    Args:
        category_distribution: Распределение по категориям.
    """
    # Используем pandas и numpy для сортировки данных
    df = pd.DataFrame(
        {
            "categories": list(category_distribution.keys()),
            "counts": list(category_distribution.values()),
        }
    )

    # Сортируем по количеству
    df_sorted = df.sort_values("counts")

    # Создаем график с улучшенным дизайном
    plt.figure(figsize=(14, 10))
    bars = plt.barh(
        df_sorted["categories"],
        df_sorted["counts"],
        color=plt.cm.viridis(np.linspace(0, 1, len(df_sorted))),
    )

    # Добавляем подписи значений с улучшенным форматированием
    max_count = df_sorted["counts"].max()
    for bar, count in zip(bars, df_sorted["counts"]):
        width = bar.get_width()
        plt.text(
            width + max_count * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{count:,}",
            ha="left",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
        )

    plt.xlabel("Количество примеров", fontsize=12)
    plt.ylabel("Категории", fontsize=12)
    plt.title("Распределение примеров по категориям DBpedia", fontsize=14, pad=20)
    plt.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()

    # Сохраняем график с высоким качеством
    plt.savefig(
        "visualization.png",
        dpi=300,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close()
