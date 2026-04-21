
## 🏎️ Sports Car Recommendation Engine

Sports Car Recommendation Engine is a Machine Learning project built to suggest the perfect high-performance vehicles to users based on their specific performance criteria. By analyzing a comprehensive dataset of sports cars, the system cleans the data and utilizes similarity algorithms to find the closest match to a user's desired specifications.


## 🚀 Key Features

Performance-Based Matching: Suggests cars based on specific user inputs like engine performance, price, and speed criteria.

Automated Data Preprocessing: Includes robust data cleaning scripts to handle missing values and format the raw dataset for accurate analysis.

Algorithm-Driven Suggestions: Utilizes Machine Learning techniques (like Cosine Similarity) to calculate mathematical closeness between different car profiles.

Scalable Logic: Designed using modular Python scripts, making it easy to plug in larger datasets or connect to a web frontend later.

## 🛠️ Tech Stack

Python: The core programming language used for scripting and logic.

Pandas: Used for extensive data manipulation, cleaning, and formatting of the dataset.

Scikit-Learn: The Machine Learning library utilized for calculating similarities and building the recommendation engine.


## 📁 Project Structure

```
Car-Recommendation/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── eslint.config.js
│   ├── package.json
│   └── package-lock.json
│
├── backend/
│   ├── server.js
│   ├── routes/
│   │   └── recommend.js
│   ├── controllers/
│   │   └── recommendController.js
│   ├── services/
│   │   └── pythonBridge.js
│   ├── package.json
│   └── package-lock.json
│
├── ml_engine/
│   ├── model/
│   │   └── car_price_model.pkl
│   ├── data/
│   │   └── sport_car_price.csv
│   ├── CR_Logic.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```


⚙️ Installation & Setup

# 1. Clone the Repository

git clone https://github.com/yourusername/car-recommendation.git
cd car-recommendation

# 2. Install Dependencies

Make sure you have Python installed, then install the required data science libraries:

pip install pandas scikit-learn

# 3. Run the System

# First, ensure your data is processed

python src/data_cleaning.py

# Run the recommendation script to see outputs

python src/recommendation_logic.py


🧠 How It Works (The Logic)

Data Ingestion: The system loads Sport car price.csv, which contains various attributes of modern sports cars.

Data Cleaning: The pandas library removes null values, standardizes text (e.g., converting strings to lowercase), and prepares numerical columns for calculation.

Feature Vectorization: The car attributes are converted into a mathematical format (vectors) using scikit-learn.

Similarity Calculation: The system calculates the similarity score between the user's requested criteria and the available cars in the dataset.

Output: The top closest matches are returned, providing a ranked list of recommended sports cars.