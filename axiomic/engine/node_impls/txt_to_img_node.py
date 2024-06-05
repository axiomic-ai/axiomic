import axiomic.protos as protos

import axiomic.providers.img_provider.img_provider as img_provider
import axiomic.configure as configure

from icecream import ic 

import axiomic.models as models

ic.configureOutput(includeContext=True)


def txt_to_img_node(node: protos.axiomic.TextToImagesNode, c, weave_node: protos.axiomic.AxiomicNode) -> str:
    prompt = c.resolve_node(node.image_prompt)

    params = node.params
    req = img_provider.ImgInferenceRequest(
        params.image_provider_name,
        params.model_name,
        params.image_width,
        params.image_height,
        prompt,
        params.num_images
    )

    resp = models.get_provider_provider().get_provider(params.image_provider_name).infer(req)
    return resp.image_list
