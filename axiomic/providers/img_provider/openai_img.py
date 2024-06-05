from openai import OpenAI

import axiomic.data.aimage as wimage

import axiomic.providers.img_provider.img_provider as img_provider
import time
import os


if "OPENAI_API_KEY" in os.environ:
    client = OpenAI()
else:
    client = None


def openai_image(prompt="a white siamese cat", model="dall-e-3", size_str="1024x1024", quality="standard", n=1):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size_str,
        quality=quality,
        n=n,
    )
    urls = [response.data[i].url for i in range(len(response.data))]
    imgs = []
    for url in urls:
        imgs.append(wimage.image_from_url(url))
    return imgs

# print(img)
# img.pretty_print()
# img.to_file('/tmp/woodchuck.png')

class OpenAiImageProviderImpl:
    def __init__(self):
        pass

    def get_default_context_params(self):
        return {
            'image_provider_name': 'openai_img',
            'image_model_name': 'dall-e-3',
            'image_width': 1024,
            'image_height': 1024,
        }
    
    def get_provider_name(self):
        return 'openai_img'

    def infer(self, req: img_provider.ImgInferenceRequest) -> img_provider.ImgInferenceResponse:
        size_str = str(req.image_width) + 'x' + str(req.image_height)
        start = time.time()
        images = openai_image(
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


