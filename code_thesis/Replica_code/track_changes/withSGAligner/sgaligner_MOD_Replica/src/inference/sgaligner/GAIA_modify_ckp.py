import torch

checkpoint = torch.load('/local/home/gmarsich/Desktop/weights+files/gat-point-rel-attr-epoch-50.pth.tar')
model_state_dict = checkpoint['model']

print(model_state_dict.keys())
print(f"\nEpoch: {checkpoint['epoch']}, Iteration: {checkpoint['iteration']}\n")

# Save the checkpoint with only the info concerning pct and gat
# Keys to be saved

# ['object_encoder.conv1.weight', 'object_encoder.conv1.bias', 'object_encoder.conv2.weight', 'object_encoder.conv2.bias',
#                 'object_encoder.conv3.weight', 'object_encoder.conv3.bias', 'object_encoder.bn1.weight', 'object_encoder.bn1.bias',
#                 'object_encoder.bn1.running_mean', 'object_encoder.bn1.running_var', 'object_encoder.bn1.num_batches_tracked', 'object_encoder.bn2.weight',
#                 'object_encoder.bn2.bias', 'object_encoder.bn2.running_mean', 'object_encoder.bn2.running_var', 'object_encoder.bn2.num_batches_tracked',
#                 'object_encoder.bn3.weight', 'object_encoder.bn3.bias', 'object_encoder.bn3.running_mean', 'object_encoder.bn3.running_var',
#                 'object_encoder.bn3.num_batches_tracked', 'object_embedding.weight', 'object_embedding.bias', 'structure_encoder.layer_stack.0.att_src',
#                 'structure_encoder.layer_stack.0.att_dst', 'structure_encoder.layer_stack.0.bias', 'structure_encoder.layer_stack.0.lin_src.weight',
#                 'structure_encoder.layer_stack.0.lin_dst.weight', 'structure_encoder.layer_stack.1.att_src', 'structure_encoder.layer_stack.1.att_dst',
#                 'structure_encoder.layer_stack.1.bias', 'structure_encoder.layer_stack.1.lin_src.weight', 'structure_encoder.layer_stack.1.lin_dst.weight',
#                 'structure_embedding.weight', 'structure_embedding.bias'] # TODO do I need 'fusion.weight' ? I guess I need that, but just 2 out of 4 things

keys_to_keep = ['object_encoder', 'structure_encoder', 'object_embedding', 'structure_embedding', 'fusion.weight']

new_state_dict = {}

for k, v in model_state_dict.items():
    if any(k.startswith(key) for key in keys_to_keep):
        if k == 'fusion.weight':
            # Keep only the first two elements of the fusion.weight tensor
            new_state_dict[k] = v[:2]
        else:
            new_state_dict[k] = v

new_checkpoint = {
    'model': new_state_dict,
    'epoch': checkpoint['epoch'],
    'iteration': checkpoint['iteration']
}

torch.save(new_checkpoint, '/local/home/gmarsich/Desktop/weights+files/gat-point-epoch-50.pth.tar')

print(f"New checkpoint saved with keys: {list(new_state_dict.keys())}")
