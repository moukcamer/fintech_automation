from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def get_models():
    return {
        "linear": LinearRegression(),
        "rf": RandomForestRegressor(n_estimators=100, random_state=42)
    }
