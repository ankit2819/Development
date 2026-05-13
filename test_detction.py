import cv2
from ultralytics import YOLO

print("Testing pedestrian detection...")
print("Make sure you're visible in the camera!")

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)

for i in range(100):  # Test for ~3 seconds
    ret, frame = cap.read()
    if ret:
        results = model(frame, verbose=False)[0]
        person_count = 0
        
        if results.boxes is not None:
            for box in results.boxes:
                if int(box.cls[0]) == 0:  # Person class
                    person_count += 1
        
        print(f"Frame {i}: Detected {person_count} persons", end="\r")
        
        cv2.imshow("Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("\n Test complete!")