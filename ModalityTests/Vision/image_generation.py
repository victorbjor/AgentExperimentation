import torch
from diffusers import FluxPipeline

# Flux diffuser backbone
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", cache_dir='.', torch_dtype=torch.bfloat16)

# "Simple vector style" Lora weights
pipe.load_lora_weights("lichorosario/flux-lora-simple-vector")

pipe = pipe.to("mps") # or cuda, or cpu, depending on system

prompt = "A cat holding a sign that says hello world"

image = pipe(
    prompt,
    height=256,
    width=256,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator('mps')
).images[0]
image.save("flux-schnell.png")

prompt = "v3ct0r style, simple flat vector art, isolated on white bg, " + prompt

image = pipe(
    prompt,
    height=256,
    width=256,
    guidance_scale=3.5,
    num_inference_steps=50,
    max_sequence_length=512,
    generator=torch.Generator('mps')
).images[0]
image.save("flux-schnell-vector.png")