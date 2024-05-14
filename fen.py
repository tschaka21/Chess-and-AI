import cv2
import torch
import numpy as np
import os
from model import NeuralNet, img_processing, label_to_fen, n_in, h1, h2, h3, h4, h5, n_out
import glob


class FENPredictor:
    def __init__(self, model_path):
        # Laden des trainierten Modells
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = NeuralNet(n_in, h1, h2, h3, h4, h5, n_out).to(self.device)
        self.model = torch.load(model_path)
        self.model.eval()
    
    def predict_fen(self, image_path):
        # Laden des Bildes und Verarbeiten
        img = cv2.imread(image_path)
        img_processed = img_processing(img)
        img_tensor = torch.FloatTensor(img_processed).to(self.device)
        
        # Vorhersage mit dem Modell
        with torch.no_grad():
            output = self.model(img_tensor)
        
        # Umwandlung der Vorhersage in einen FEN-Code
        predicted_labels = output.view(len(output), -1).argmax(1).cpu().numpy().astype(np.int32).tolist()
        predicted_fen = label_to_fen(predicted_labels)
        
        return predicted_fen

# Verwendung der Klasse
if __name__ == "__main__":
    model_path = 'model_chess.pth'
    predictor = FENPredictor(model_path)
    
    # Dateipfad zum Ordner mit Bildern
    image_folder_path = glob.glob(r"C:\Users\KaiTs\Documents\Data Science\Datasets\Chess\fen\*.jpeg")
    
    # Vorhersage des FEN-Codes für jedes Bild im Ordner
    for image_path in image_folder_path:
        predicted_fen = predictor.predict_fen(image_path)
        print(f"Predicted FEN Code for {image_path}: {predicted_fen}")

import pandas as pd
def compare_with_csv(predicted_fen, csv_file_path):
    
    df = pd.read_csv(csv_file_path)
    
    # Durchführung des Abgleichs
    matching_rows = df[df['FEN'].isin(predicted_fen)]
    
    return matching_rows['Evaluation'].tolist(), matching_rows['Move'].tolist()



# Verwendung der Funktion
csv_file_path = glob.glob(r"C:\Users\KaiTs\Documents\Data Science\Datasets\Chess Data\tactic_evals.csv")[0]
predicted_fen_list = [predicted_fen]  # FEN-Code in eine Liste einbetten
evaluations, best_moves = compare_with_csv(predicted_fen_list, csv_file_path)
print(predicted_fen_list)


# Ergebnisse anzeigen
for evaluation, best_move in zip(evaluations, best_moves):
    print("Evaluation:", evaluation)
    print("Best Move:", best_move)
