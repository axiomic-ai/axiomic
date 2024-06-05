import os
from together import Together
import axiomic.data.aimage as wimage
import axiomic.providers.img_provider.img_provider as img_provider
import time

if "TOGETHER_API_KEY" in os.environ:
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
else:
    client = None

def gen_image(prompt="a white siamese cat", model="dall-e-3", size_str="1024x1024", quality="standard", n=1):
    response = client.images.generate(
        prompt=prompt,
        model=model,
        steps=10,
        n=1,
    )
    return [wimage.image_from_base64(response.data[0].b64_json)]


class TogetherImageProviderImpl:
    def __init__(self):
        pass

    def get_default_context_params(self):
        return {
            'image_provider_name': 'together_img',
            'image_model_name': 'stabilityai/stable-diffusion-2-1', # 'stabilityai/stable-diffusion-xl-base-1.0',
            'image_width': 1024,
            'image_height': 1024,
        }
    
    def get_provider_name(self):
        return 'together_img'

    def infer(self, req: img_provider.ImgInferenceRequest) -> img_provider.ImgInferenceResponse:
        size_str = str(req.image_width) + 'x' + str(req.image_height)
        start = time.time()
        images = gen_image(
            prompt=req.image_prompt,
            model=req.model_name,
            size_str=size_str,
            quality="standard",
            n=req.num_images
        )
        end = time.time()

        return img_provider.ImgInferenceResponse(
            req.img_provider_name,
            req.model_name,
            req.image_width,
            req.image_height,
            req.image_prompt,
            req.num_images,
            images,
            end - start
        )


