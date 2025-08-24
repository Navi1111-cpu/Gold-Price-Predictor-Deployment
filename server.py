from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import joblib
import numpy as np

# Load your trained model and scaler
try:
    model = joblib.load('model_final.joblib')
    scaler = joblib.load('scaler.joblib')
    print("✅ Model and scaler loaded successfully!")
except:
    print("❌ Error: Could not load model files. Make sure model_final.joblib and scaler.joblib exist.")
    exit()

# Create FastAPI app
app = FastAPI(title="Gold Price Predictor")

# Allow cross-origin requests (so HTML can call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home page - HTML code embedded directly
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gold Price Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        input:focus { border-color: #4CAF50; outline: none; }
        .predict-btn { width: 100%; padding: 15px; background: #4CAF50; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; margin-top: 20px; }
        .predict-btn:hover { background: #45a049; }
        .results { margin-top: 30px; padding: 20px; background: #f9f9f9; border-radius: 5px; border-left: 5px solid #4CAF50; }
        .result-price { font-size: 24px; font-weight: bold; color: #4CAF50; margin-bottom: 10px; }
        .loading { text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥇 Gold Price Predictor</h1>
            <p>AI-Powered GLD ETF Price Prediction</p>
        </div>
        
        <div class="form-group">
            <label>Current GLD Price ($)</label>
            <input type="number" id="current-gld" value="87.50" step="0.01">
        </div>
        
        <div class="form-group">
            <label>S&P 500 Return (%)</label>
            <input type="number" id="spx-return" value="0.5" step="0.001">
        </div>
        
        <div class="form-group">
            <label>USO (Oil ETF) Return (%)</label>
            <input type="number" id="uso-return" value="-1.0" step="0.001">
        </div>
        
        <div class="form-group">
            <label>SLV (Silver ETF) Return (%)</label>
            <input type="number" id="slv-return" value="0.8" step="0.001">
        </div>
        
        <div class="form-group">
            <label>EUR/USD Return (%)</label>
            <input type="number" id="eur-usd-return" value="0.1" step="0.001">
        </div>
        
        <div class="form-group">
            <label>GLD Previous Day Return (%)</label>
            <input type="number" id="gld-lag1" value="0.3" step="0.001">
        </div>
        
        <div class="form-group">
            <label>GLD Two Days Ago Return (%)</label>
            <input type="number" id="gld-lag2" value="-0.2" step="0.001">
        </div>
        
        <div class="form-group">
            <label>GLD 3-Day Volatility</label>
            <input type="number" id="gld-volatility" value="0.015" step="0.001">
        </div>
        
        <button class="predict-btn" onclick="predictGoldPrice()">🔮 Predict Tomorrow's GLD Price</button>
        
        <div id="results" style="display: none;" class="results">
            <div class="result-price" id="predicted-price">$0.00</div>
            <div><strong>Current Price:</strong> $<span id="current-price">0.00</span></div>
            <div><strong>Predicted Return:</strong> <span id="predicted-return">0.00</span>%</div>
            <div><strong>Price Change:</strong> $<span id="price-change">0.00</span></div>
        </div>
        
        <div id="loading" style="display: none;" class="loading">
            <p>🔄 Calculating prediction...</p>
        </div>
    </div>

    <script>
        async function predictGoldPrice() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            const data = {
                current_gld_price: parseFloat(document.getElementById('current-gld').value),
                spx_return: parseFloat(document.getElementById('spx-return').value),
                uso_return: parseFloat(document.getElementById('uso-return').value),
                slv_return: parseFloat(document.getElementById('slv-return').value),
                eur_usd_return: parseFloat(document.getElementById('eur-usd-return').value),
                gld_lag1: parseFloat(document.getElementById('gld-lag1').value),
                gld_lag2: parseFloat(document.getElementById('gld-lag2').value),
                gld_volatility_3: parseFloat(document.getElementById('gld-volatility').value)
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('loading').style.display = 'none';
                
                if (result.success) {
                    document.getElementById('predicted-price').textContent = '

# Prediction endpoint
@app.post("/predict")
def predict(data: dict):
    try:
        # Get data from frontend
        current_price = float(data['current_gld_price'])
        spx_return = float(data['spx_return']) / 100
        uso_return = float(data['uso_return']) / 100
        slv_return = float(data['slv_return']) / 100
        eur_usd_return = float(data['eur_usd_return']) / 100
        gld_lag1 = float(data['gld_lag1']) / 100
        gld_lag2 = float(data['gld_lag2']) / 100
        volatility = float(data['gld_volatility_3'])
        
        # Prepare features (same order as your training)
        features = np.array([[
            spx_return,
            uso_return,
            slv_return,
            eur_usd_return,
            gld_lag1,
            gld_lag2,
            volatility
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        predicted_return = model.predict(features_scaled)[0]
        
        # Convert to price
        predicted_price = current_price * np.exp(predicted_return)
        
        # Calculate changes
        price_change = predicted_price - current_price
        percent_change = (price_change / current_price) * 100
        
        # Return results
        return {
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'current_price': current_price,
            'predicted_return': round(predicted_return * 100, 4),
            'price_change': round(price_change, 2),
            'percentage_change': round(percent_change, 2)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Health check
@app.get("/health")
def health():
    return {"status": "running", "message": "Gold predictor is working!"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Gold Price Predictor...")
    print("📊 Open your browser and go to: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000) + result.predicted_price;
                    document.getElementById('current-price').textContent = result.current_price.toFixed(2);
                    document.getElementById('predicted-return').textContent = result.predicted_return.toFixed(3);
                    document.getElementById('price-change').textContent = result.price_change.toFixed(2);
                    document.getElementById('results').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                alert('Failed to get prediction: ' + error);
            }
        }
    </script>
</body>
</html>
    """

# Prediction endpoint
@app.post("/predict")
def predict(data: dict):
    try:
        # Get data from frontend
        current_price = float(data['current_gld_price'])
        spx_return = float(data['spx_return']) / 100
        uso_return = float(data['uso_return']) / 100
        slv_return = float(data['slv_return']) / 100
        eur_usd_return = float(data['eur_usd_return']) / 100
        gld_lag1 = float(data['gld_lag1']) / 100
        gld_lag2 = float(data['gld_lag2']) / 100
        volatility = float(data['gld_volatility_3'])
        
        # Prepare features (same order as your training)
        features = np.array([[
            spx_return,
            uso_return,
            slv_return,
            eur_usd_return,
            gld_lag1,
            gld_lag2,
            volatility
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        predicted_return = model.predict(features_scaled)[0]
        
        # Convert to price
        predicted_price = current_price * np.exp(predicted_return)
        
        # Calculate changes
        price_change = predicted_price - current_price
        percent_change = (price_change / current_price) * 100
        
        # Return results
        return {
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'current_price': current_price,
            'predicted_return': round(predicted_return * 100, 4),
            'price_change': round(price_change, 2),
            'percentage_change': round(percent_change, 2)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Health check
@app.get("/health")
def health():
    return {"status": "running", "message": "Gold predictor is working!"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Gold Price Predictor...")
    print("📊 Open your browser and go to: http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)