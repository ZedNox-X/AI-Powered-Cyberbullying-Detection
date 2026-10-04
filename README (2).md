# 🛡️ CyberShield AI — Cyberbullying Detection System

An educational AI/NLP web application that classifies online messages into **non-bullying**, **bullying**, or **severe-bullying** categories.

## Features

- Machine-learning text classification using TF-IDF + Logistic Regression
- Three-class detection
- Confidence score
- Flask web interface
- SQLite analysis history
- Admin dashboard
- JSON REST API
- Health-check endpoint
- Reproducible model-training script
- Responsive UI

## Important note

The included dataset is a **small demonstration dataset created for this repository**. It is not suitable for production moderation or measuring real-world model performance. For a research or production system, replace it with a properly licensed, diverse, human-annotated dataset and evaluate precision, recall, F1-score, subgroup performance, and false-positive/false-negative rates.

## Project structure

```text
cyberbullying-detection/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── dataset/
│   └── cyberbullying_dataset.csv
├── model/
│   └── README.md
├── scripts/
│   └── train_model.py
├── templates/
├── static/
├── database/
└── tests/
```

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/cyberbullying-detection.git
cd cyberbullying-detection
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Train the model

```bash
python scripts/train_model.py
```

This creates `model/bullying_model.pkl` and `model/vectorizer.pkl`.

## 5. Start the application

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Admin dashboard

Open `/admin/login`.

Development defaults:

- Username: `admin`
- Password: `admin123`

For deployment, set `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `SECRET_KEY` environment variables. Do not commit real credentials.

## API

### POST `/api/predict`

Request:

```json
{
  "text": "Example message to analyze"
}
```

Response:

```json
{
  "text": "Example message to analyze",
  "label": "non-bullying",
  "confidence": 0.72
}
```

Example with curl:

```bash
curl -X POST http://127.0.0.1:5000/api/predict \\
  -H "Content-Type: application/json" \\
  -d '{"text":"You are doing a great job"}'
```

## Security considerations

This is a student/portfolio project. Before production use, add secure password hashing, CSRF protection, rate limiting, HTTPS, stronger session configuration, access-control hardening, privacy controls, content retention policies, audit logging, and a professionally validated model.

## Future improvements

- Transformer-based model such as DistilBERT/BERT
- Multilingual detection
- Explainable AI with highlighted terms
- Human moderator review workflow
- User reporting system
- Real-time social-platform moderation API
- Bias/fairness evaluation
- Docker deployment

## License

MIT License. See `LICENSE`.

## Upload to GitHub

After downloading this project:

```bash
git init
git add .
git commit -m "Initial CyberShield AI project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cyberbullying-detection.git
git push -u origin main
```

Then, on a fresh machine, follow the installation and model-training steps above.
