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
            return self._create_placeholder(prompt, width, height)
            
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")
        return self._create_placeholder(prompt, width, height)