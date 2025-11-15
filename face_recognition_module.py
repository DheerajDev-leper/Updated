import cv2
import mediapipe as mp
import numpy as np
import time
import os

# Mediapipe face detection
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

# Folder where known faces will be stored
KNOWN_FACE_DIR = "known_faces"

# ----------------------
# Load Known Face Embeddings
# ----------------------
def load_known_faces():
    known_encodings = []
    known_names = []

    if not os.path.exists(KNOWN_FACE_DIR):
        os.makedirs(KNOWN_FACE_DIR)

    for file in os.listdir(KNOWN_FACE_DIR):
        if file.endswith(".npy"):
            encoding = np.load(os.path.join(KNOWN_FACE_DIR, file))
            name = file.replace(".npy", "")
            known_encodings.append(encoding)
            known_names.append(name)

    print(f"[INFO] Loaded {len(known_names)} known faces.")
    return known_encodings, known_names

# ----------------------
# Save a new face
# ----------------------
def save_new_face(embedding, name):
    np.save(f"{KNOWN_FACE_DIR}/{name}.npy", embedding)
    print(f"[INFO] Saved new face for {name}")

# ----------------------
# Generate face embedding using FaceMesh landmarks
# ----------------------
def generate_embedding(landmarks):
    points = []
    for lm in landmarks.landmark:
        points.append([lm.x, lm.y, lm.z])
    return np.array(points).flatten()


# ----------------------
# Start Face Recognition
# ----------------------
def start_face_recognition():
    cap = cv2.VideoCapture(0)

    face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    known_encodings, known_names = load_known_faces()

    print("[INFO] Starting camera... press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face detection
        results = face_detection.process(rgb)

        if results.detections:
            for detection in results.detections:
                # Extract bounding box
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = x1 + int(bbox.width * w)
                y2 = y1 + int(bbox.height * h)

                face_roi = rgb[y1:y2, x1:x2]

                # Face landmarks (for embedding)
                mesh_results = face_mesh.process(face_roi)
                name = "Unknown"

                if mesh_results.multi_face_landmarks:
                    embedding = generate_embedding(mesh_results.multi_face_landmarks[0])

                    # Compare with known faces
                    if len(known_encodings) > 0:
                        distances = [np.linalg.norm(embedding - enc) for enc in known_encodings]
                        min_dist = min(distances)

                        if min_dist < 0.55:  # threshold
                            name = known_names[distances.index(min_dist)]

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Pi Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
