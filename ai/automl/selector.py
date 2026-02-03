from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def select_best_model(X, y, models):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    best_model = None
    best_score = float("inf")

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        score = mean_absolute_error(y_test, preds)

        if score < best_score:
            best_score = score
            best_model = (name, model)

    return best_model, best_score
