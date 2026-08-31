from tools.calculator import average


def summarize_values(label_value_pairs):
    values = [v for _, v in label_value_pairs if v is not None]
    if not values:
        return {}
    return {
        "count": len(values),
        "average": average(values),
        "max": max(values),
        "min": min(values)
    }


def rank_items(label_value_pairs, descending=True):
    items = [x for x in label_value_pairs if x[1] is not None]
    return sorted(items, key=lambda x: x[1], reverse=descending)
