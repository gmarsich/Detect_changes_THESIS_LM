import cv2
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def segment_objects(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Otsu's thresholding to segment foreground objects
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Invert the binary image
    thresh = cv2.bitwise_not(thresh)
    
    # Perform morphological operations to clean up the thresholded image
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small contours and get bounding boxes
    objects = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            objects.append((x, y, x + w, y + h))
    
    return objects

def find_relationships(objects):
    relationships = []
    num_objects = len(objects)
    
    # Simple spatial relationship based on proximity
    for i in range(num_objects):
        for j in range(num_objects):
            if i != j:
                if are_close(objects[i], objects[j]):
                    relationships.append({
                        "subject_id": i,
                        "object_id": j,
                        "predicate": "near"
                    })
    
    return relationships

def are_close(box1, box2, threshold=50):
    # Check if boxes are close based on center distance
    x1, y1, _, _ = box1
    x2, y2, _, _ = box2
    center_dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return center_dist < threshold

def visualize_scene_graph(image, objects, relationships, output_path):
    # Draw bounding boxes on the image
    for (x1, y1, x2, y2) in objects:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Draw relationships
    G = nx.DiGraph()
    for i, (x1, y1, _, _) in enumerate(objects):
        G.add_node(i, pos=(x1, y1))
    
    for rel in relationships:
        G.add_edge(rel["subject_id"], rel["object_id"], label=rel["predicate"])
    
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_edge_attributes(G, 'label')
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.savefig(output_path)  # Save the image
    plt.close()

def get_scene_graph(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Segment objects
    objects = segment_objects(image)
    
    # Find relationships
    relationships = find_relationships(objects)
    
    return objects, relationships

# Example usage
image_path = "Fishes.jpg"
output_path = "output_scene_graph.png"  # Define output path
objects, relationships = get_scene_graph(image_path)
visualize_scene_graph(cv2.imread(image_path), objects, relationships, output_path)
