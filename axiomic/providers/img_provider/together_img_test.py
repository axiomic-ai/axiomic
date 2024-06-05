
import axiomic.providers.img_provider.together_img as together_img


def test_image_gen():
    img = together_img.gen_image("a white siamese cat", "stabilityai/stable-diffusion-xl-base-1.0", "1024x1024", "standard", 1)


if __name__ == '__main__':
    test_image_gen()
