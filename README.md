# 🛍️ AI Product Description Generator API

This project provides an AI-powered Flask API that accepts a product image, generates a caption using GPT-4 Vision, and then produces a full e-commerce product description based on the image.

## 🚀 Features
- Upload a product image
- Get a smart, descriptive image caption via GPT-4 Vision
- Generate SEO-friendly product title, description, and bullet points
- Swagger UI for interactive API testing
- Dockerized for easy deployment

---

## 📦 Requirements
- Python 3.10+
- OpenAI API key (with GPT-4 Vision access)
- Docker (optional, for containerization)

---

## 🧪 API Endpoints

### `POST /generate-description-from-image`
Generates a full product description from an uploaded image.

#### 🔸 Form Data Parameters:
- `image` (file): The product image (JPEG/PNG)
- `tone` (string, optional): Description tone (e.g., Professional, Friendly, Luxury)

#### ✅ Example Response:
```json
{
  "caption": "A minimalist bamboo laptop stand with a slot for smartphones.",
  "description": "### Bamboo Laptop Stand\nErgonomically designed..."
}
```

### 🌐 Swagger UI:
Access the interactive docs at: `http://localhost:5000/apidocs`

---

## 🐳 Run with Docker

### 1. Build the Docker image:
```bash
docker build -t product-description-api .
```

### 2. Run the container:
```bash
docker run --env-file .env -p 5000:5000 product-description-api
```

Make sure your `.env` file includes:
```env
OPENAI_API_KEY=sk-xxxxx...
```

---

## 🧰 Project Structure
```
├── product_description_api.py  # Main Flask app
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container config
├── .env                        # Environment variables (not committed)
├── README.md                   # This file
```

---

## 📋 Example Curl Request
```bash
curl -X POST http://localhost:5000/generate-description-from-image \
  -F "image=@./sample.jpg" \
  -F "tone=Luxury"
```

---

## ✨ Future Improvements
- Add CSV export
- Add support for batch product generation
- Integrate with Shopify, WooCommerce, etc.

---

## 🧠 Powered By
- OpenAI GPT-4 Vision
- Flask + Swagger + Docker

---

## 👨‍💻 Author
Built with 💡 by Mindgraph