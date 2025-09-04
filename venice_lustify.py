import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO

# Define a class to hold our app's logic
class ImageGeneratorApp:
    def _create_placeholder(self, text, width, height):
        """Creates a placeholder image for fallbacks."""
        img = Image.new('RGB', (width, height), color = (73, 109, 137))
        # No easy way to draw text without more libraries, so we'll keep it simple
        return img

    def generate_with_flux(self, prompt, width=1024, height=1024, steps=4):
        """Working Flux API call"""
        try:
            with st.spinner("🚀 Generating with Flux-1-Schnell..."):
                api_url = "https://evalstate-flux1-schnell.hf.space/run/predict"
                
                payload = {
                    "data": [
                        prompt,
                        width,
                        height, 
                        steps,
                        True,  # randomize_seed
                        random.randint(0, 2147483647)
                    ]
                }
                
                response = requests.post(api_url, json=payload, timeout=120)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'data' in result and result['data']:
                        image_path = result['data'][0]
                        
                        # Construct URL
                        if not image_path.startswith('http'):
                            image_url = f"https://evalstate-flux1-schnell.hf.space/file={image_path}"
                        else:
                            image_url = image_path
                        
                        # Download image
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            img = Image.open(BytesIO(img_response.content))
                            return img
                
                # Fallback to placeholder if API fails
                st.warning("Image generation failed or returned an invalid response. Showing a placeholder.")
                return self._create_placeholder(prompt, width, height)
                
        except Exception as e:
            st.error(f"An error occurred during generation: {str(e)}")
            return self._create_placeholder(prompt, width, height)

    def run(self):
        """This is the main method that runs the Streamlit UI"""
        st.set_page_config(layout="wide")
        st.title("🎨 AI Image Generator")

        prompt = st.text_input("Enter your image prompt:", "A majestic lion on a grassy plain")

        if st.button("Generate Image"):
            if prompt:
                generated_image = self.generate_with_flux(prompt)
                if generated_image:
                    st.image(generated_image, caption="Generated Image", width='stretch')
            else:
                st.warning("Please enter a prompt.")

# This is the "Start Cooking!" command.
# It tells Python to run the app when the script is executed.
if __name__ == "__main__":
    app = ImageGeneratorApp()
    app.run()

