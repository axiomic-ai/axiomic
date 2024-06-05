
from typing import List, Tuple

import axiomic.logalytics as logalytics

import dataclasses


@dataclasses.dataclass
class ImgInferenceRequest:
    img_provider_name: str
    model_name: str
    image_width: int
    image_height: int
    image_prompt: str
    num_images: int


@dataclasses.dataclass
class ImgInferenceResponse:
    img_provider_name: str
    model_name: str
    image_width: int
    image_height: int
    image_prompt: str
    num_images: int
    image_list: List
    duration_s: float


class ImgProvider:
    def __init__(self, img_provider_impl):
        self.img_provider_impl = img_provider_impl

    def get_default_context_params(self):
        return self.img_provider_impl.get_default_context_params()
    
    def get_provider_name(self):
        return self.img_provider_impl.get_provider_name()

    def infer(self, req: ImgInferenceRequest) -> ImgInferenceResponse:
        provider_name = req.img_provider_name
        info = {
            'image_model_name': req.model_name,
            'image_width': req.image_width,
            'image_height': req.image_height,
            'image_prompt': req.image_prompt,
            'num_images': req.num_images,
            'provider_name': provider_name
        }

        with logalytics.ImageInference(provider_name, info) as c:
            resp = self.img_provider_impl.infer(req)
            c.end(image_list=resp.image_list, duration_s=resp.duration_s, image_model_name=resp.model_name,
                  image_width=resp.image_width, image_height=resp.image_height, provider_name=resp.img_provider_name)
        return resp
        #    c.end(model_name=llm_history_inference.model_name, input_tokens=resp.input_tokens, output_tokens=resp.output_tokens, duration_s=resp.duration_s, response=resp.response)
        #    return resp

