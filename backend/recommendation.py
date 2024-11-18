import numpy as np
from scipy.sparse.linalg import svds
import itertools


type_map = {"chair": 0, "table": 1, "couch": 2}
color_map = {"black": 0, "red": 1, "green": 2}
style_map = {"modern": 0, "classic": 1}
material_map = {"wooden": 0, "metal": 1, "fabric": 2}

type_map_rev = {v: k for k, v in type_map.items()}
color_map_rev = {v: k for k, v in color_map.items()}
style_map_rev = {v: k for k, v in style_map.items()}
material_map_rev = {v: k for k, v in material_map.items()}
feature_values = {
    "type": list(type_map.values()),
    "color": list(color_map.values()),
    "style": list(style_map.values()),
    "material": list(material_map.values()),
}

items = []
item_descriptions = []
for combination in itertools.product(
    feature_values["type"],
    feature_values["color"],
    feature_values["style"],
    feature_values["material"],
):
    item = {
        "type": combination[0],
        "color": combination[1],
        "style": combination[2],
        "material": combination[3],
    }
    items.append(item)
    description = (
        f"{color_map_rev[item['color']].capitalize()} {material_map_rev[item['material']].capitalize()} "
        f"{type_map_rev[item['type']].capitalize()} ({style_map_rev[item['style']].capitalize()})"
    )
    item_descriptions.append(description)

num_items = len(items)

num_users = 30
rating_matrix = np.zeros((num_users, num_items))
user_groups = {
    0: {"type": 0, "color": 0, "material": 0},  # Group 0 prefers Black Wooden Chairs
    1: {"type": 1, "color": 1, "material": 1},  # Group 1 prefers Red Metal Tables
    2: {"type": 2, "color": 2, "material": 2},  # Group 2 prefers Green Fabric Couches
}
for user_id in range(num_users):
    group_id = user_id % 3
    group_prefs = user_groups[group_id]
    for item_id, item in enumerate(items):
        match = all(item[feature] == group_prefs[feature] for feature in group_prefs)
        if match:
            rating_matrix[user_id, item_id] = np.random.uniform(4, 5)
        else:
            rating_matrix[user_id, item_id] = np.random.uniform(1, 3)


def perform_svd(rating_matrix, k=5):
    user_ratings_mean = np.mean(rating_matrix, axis=1)
    R_demeaned = rating_matrix - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k=k)
    sigma = np.diag(sigma)
    all_user_predicted_ratings = np.dot(
        np.dot(U, sigma), Vt
    ) + user_ratings_mean.reshape(-1, 1)

    return all_user_predicted_ratings


predicted_ratings = perform_svd(rating_matrix)


def parse_user_input(input_str):
    words = input_str.lower().split()
    user_features = {"type": None, "color": None, "style": None, "material": None}
    for word in words:
        if word in type_map:
            user_features["type"] = word
        elif word in color_map:
            user_features["color"] = word
        elif word in style_map:
            user_features["style"] = word
        elif word in material_map:
            user_features["material"] = word
    return user_features


def recommend_items_ml(
    user_input_features,
    items,
    item_descriptions,
    predicted_ratings,
    num_recommendations=3,
):
    new_user_id = rating_matrix.shape[0]
    new_user_ratings = np.zeros((1, num_items))
    avg_predicted_ratings = predicted_ratings.mean(axis=0)
    user_features = {}
    for feature, value in user_input_features.items():
        if value is not None:
            if feature == "type":
                user_features["type"] = type_map[value]
            elif feature == "color":
                user_features["color"] = color_map[value]
            elif feature == "style":
                user_features["style"] = style_map[value]
            elif feature == "material":
                user_features["material"] = material_map[value]

    matching_items_indices = []
    for idx, item in enumerate(items):
        match = all(
            item.get(feature) == user_features[feature] for feature in user_features
        )
        if match:
            matching_items_indices.append(idx)

    if not matching_items_indices:
        print("No items match your specified features.")
        return []
    matching_items_ratings = avg_predicted_ratings[matching_items_indices]

    top_indices = np.argsort(-matching_items_ratings)[:num_recommendations]
    recommended_item_indices = [matching_items_indices[i] for i in top_indices]

    recommendations = []
    for idx in recommended_item_indices:
        item = items[idx]
        recommendation = {
            "type": type_map_rev[item["type"]],
            "color": color_map_rev[item["color"]],
            "style": style_map_rev[item["style"]],
            "material": material_map_rev[item["material"]],
            "predicted_rating": round(avg_predicted_ratings[idx], 2),
        }
        recommendations.append(recommendation)

    return recommendations


def give_recommendation(parameters):
    user_input_features = parse_user_input(parameters)
    
    recommendations = recommend_items_ml(
        user_input_features, items, item_descriptions, predicted_ratings
    )

    if recommendations:
        result = ["\nRecommended items:"]
        for rec in recommendations:
            result.append(
                f"- Type: {rec['type'].capitalize()}, Color: {rec['color'].capitalize()}, "
                f"Style: {rec['style'].capitalize()}, Material: {rec['material'].capitalize()}, "
                f"Predicted Rating: {rec['predicted_rating']}"
            )
        return '\n'.join(result)
    else:
        return "No recommendations found based on your preferences."
