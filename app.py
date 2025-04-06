from flask import Flask, request, jsonify
import openai
import os
import base64
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from flask_cors import CORS
from flasgger import Swagger, swag_from

app = Flask(__name__)
CORS(app)
Swagger(app)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route('/')
def health():
    return "✅ Product Description API is up. Use /generate-description-from-image to generate full output."

@app.route('/generate-description-from-image', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'image',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Product image to describe'
        },
        {
            'name': 'tone',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Tone of the product description (e.g., Professional, Friendly, Luxury)'
        }
    ],
    'responses': {
        200: {
            'description': 'Full product description generated from image',
            'examples': {
                'application/json': {
                    'caption': 'A sleek stainless steel travel mug with leak-proof lid.',
                    'description': '### Travel Mug\nStay hot or cold longer with this leak-proof stainless steel mug...'
                }
            }
        }
    }
})
def generate_description_from_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    tone = request.form.get("tone", "Professional")

    try:
        image = Image.open(request.files['image']).convert("RGB")
        b64_image = image_to_base64(image)

        vision_response = openai.ChatCompletion.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this product as if it's for an e-commerce listing."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        caption = vision_response["choices"][0]["message"]["content"]

        prompt = f"""
You are an expert e-commerce copywriter. Based on the following product info, write:
1. A catchy product title
2. A 2–3 line engaging product description
3. 4-5 bullet points highlighting benefits

Tone: {tone}

Product Info:
{caption.strip()}

Return in Markdown format with clear sections.
"""

        description_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = description_response["choices"][0]["message"]["content"]

        return jsonify({"caption": caption, "description": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
