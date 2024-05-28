import cv2
import torch
import matplotlib.pyplot as plt
import networkx as nx
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F

# Load the image
image_path = "Animals.png"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert image to tensor
image_tensor = F.to_tensor(image_rgb)

# Load pre-trained Faster R-CNN model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Perform object detection
with torch.no_grad():
    predictions = model([image_tensor])[0]

# Extract detected objects
boxes = predictions['boxes'].cpu().numpy()
scores = predictions['scores'].cpu().numpy()
labels = predictions['labels'].cpu().numpy()

# Filter boxes with a score threshold
score_threshold = 0.5
filtered_indices = scores > score_threshold
boxes = boxes[filtered_indices]
labels = labels[filtered_indices]

# Hypothetical relationship model (implement your own or use an existing one)
class SceneGraphModel:
    def predict_relationships(self, image, boxes, classes):
        # Placeholder for relationship prediction
        # Should return a list of dictionaries with subject_id, object_id, and predicate
        return [
            {"subject_id": 0, "object_id": 1, "predicate": "holding"}
        ]

# Relationship Detection
sgg_model = SceneGraphModel()
relationships = sgg_model.predict_relationships(image, boxes, labels)

# Scene Graph Construction
scene_graph = {
    "objects": [],
    "relationships": []
}

for i, box in enumerate(boxes):
    scene_graph["objects"].append({
        "id": i,
        "class": labels[i],
        "bbox": box.tolist()
    })

for rel in relationships:
    scene_graph["relationships"].append({
        "subject_id": rel["subject_id"],
        "object_id": rel["object_id"],
        "predicate": rel["predicate"]
    })

print(scene_graph)

# Visualization
def visualize_scene_graph(image, scene_graph, output_image_path, output_graph_path):
    # Draw bounding boxes on the image
    for obj in scene_graph["objects"]:
        bbox = obj["bbox"]
        class_id = obj["class"]
        cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        cv2.putText(image, str(class_id), (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.savefig(output_image_path)
    plt.close()

    # Draw the scene graph using networkx
    G = nx.DiGraph()

    for obj in scene_graph["objects"]:
        G.add_node(obj["id"], label=str(obj["class"]))

    for rel in scene_graph["relationships"]:
        G.add_edge(rel["subject_id"], rel["object_id"], label=rel["predicate"])

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Scene Graph")
    plt.savefig(output_graph_path)
    plt.close()

# Visualize the results
output_image_path = "output_detected_image.jpg"
output_graph_path = "output_scene_graph.png"
visualize_scene_graph(image_rgb.copy(), scene_graph, output_image_path, output_graph_path)
