import sys
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    
    if len(sys.argv) < 4:
        print("Usage: python facial_attribute_script.py <base_photo_path> <frame_folder_path>")
        sys.exit(1)
        
    base_photo_path = sys.argv[1]  # The folder name is passed as a command-line argument
    frame_folder_path = sys.argv[2]
    result_path = sys.argv[3]

    analysis_results = []

    # find all instances of zuckerberg across images
    dfs = DeepFace.find(
        img_path=base_photo_path,
        db_path=frame_folder_path,
        enforce_detection=False,
    )
    
    # get the first item, one per person
    df = dfs[0]

    for index, instance in tqdm(df.iterrows(), total=len(df), desc="Processing images"):
        source_path = instance["identity"]
        source_img_bgr = cv2.imread(source_path)

        # extract facial area of the source image
        x = instance["target_x"]
        y = instance["target_y"]
        w = instance["target_w"]
        h = instance["target_h"]
        
        # extract face
        source_img_bgr = source_img_bgr[y : y + h, x : x + w]

        # Convert BGR to RGB for correct color display
        source_img_rgb = cv2.cvtColor(source_img_bgr, cv2.COLOR_BGR2RGB)

        # Analyze the face
        try:
            analysis = DeepFace.analyze(
                img_path=source_img_bgr,  # Use the cropped BGR image
                actions=["age", "gender", "race", "emotion"],
                enforce_detection=False,
                silent=True,
            )[0]
        except Exception as e:
            print("errored image:", source_path)
            # Show the image
            plt.imshow(source_img_rgb)
            plt.axis('off')
            plt.show()
            raise e
        
        # Add the image path to the analysis dictionary
        analysis["image_path"] = source_path
        
        # Append analysis to the results list
        analysis_results.append(analysis)

    # Convert the list of dictionaries to a pandas DataFrame
    analysis_df = pd.DataFrame(analysis_results)
    
    # Display or save the resulting DataFrame
    analysis_df.to_csv(f"{result_path}analysis_results.csv", index=False)
