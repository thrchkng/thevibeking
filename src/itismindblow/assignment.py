"""
Анализ датасета DBpedia (14 категорий).

ЗАДАНИЕ:
Загрузите датасет DBpedia, анализируйте распределение по 14 категориям,
выполните статистический анализ текстов и выявите топ слова по категориям.

ТРЕБОВАНИЯ:
- Загрузить датасет: load_dataset()
- Провести анализ распределения по 14 категориям
- Вычислить статистику заголовков и контента
- Найти топ-25 слов для каждой категории
- Создать bar chart распределения
- Сохранить результаты в dbpedia_results.json
"""

import json
from typing import Dict, List, Any

import pandas as pd
from datasets import load_dataset

from dbpedia_modules import (
    analyze_text_statistics,
    create_visualization,
    extract_top_words_by_category,
    get_category_name,
)


def load_dbpedia_dataset() -> List[Dict[str, Any]]:
    """
    Загружает датасет DBpedia.

    Returns:
        List[Dict]: Список примеров с полями 'title', 'content', 'label'.
    """
    dataset = load_dataset("dbpedia_14", split="train")
    # Используем pandas для эффективной конвертации
    df = pd.DataFrame(dataset)
    # Конвертируем в список словарей
    samples = df[["title", "content", "label"]].to_dict("records")
    return samples


def analyze_category_distribution(dataset: List[Dict[str, Any]]):
    """
    Анализирует распределение по 14 категориям.

    Args:
        dataset: Список примеров с полем 'label'.

    Returns:
        Dict: Распределение по категориям {category_name: count}.
    """
    distribution = {}

    # Подсчитываем количество для каждой категории
    for label in range(14):  # DBpedia имеет 14 категорий
        category_name = get_category_name(label)
        count = sum(1 for item in dataset if item["label"] == label)
        distribution[category_name] = count

    return distribution


def main() -> None:
    """
    Основная функция анализа DBpedia.

    Загружает данные, выполняет анализ и сохраняет результаты.
    """
    print("Загрузка датасета DBpedia...")
    dataset = load_dbpedia_dataset()

    print("Анализ распределения по категориям...")
    category_distribution = analyze_category_distribution(dataset)

    print("Анализ статистики текстов...")
    text_stats = analyze_text_statistics(dataset)

    print("Извлечение топ слов по категориям...")
    top_words = extract_top_words_by_category(dataset, top_n=25)

    print("Создание визуализации...")
    create_visualization(category_distribution)

    # Сохранение результатов с общим количеством образцов
    results = {
        "dataset": "dbpedia_14",
        "total_samples": len(dataset),
        "category_distribution": category_distribution,
        "text_statistics": text_stats,
        "top_words_by_category": top_words,
    }

    with open("dbpedia_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Анализ завершен! Результаты сохранены в dbpedia_results.json")
    print(f"Всего обработано примеров: {len(dataset)}")
    print(f"Количество категорий: {len(category_distribution)}")


if __name__ == "__main__":
    main()
