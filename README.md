# RECEIPT-IDENTIFICATION
Is this receipt a “Walmart” receipt – Yes/No?

The input_folder in following 3 python files sould be replaced with the folder of the photos in your computer.

1. pytesseract_test: extract words from photos                
   output: ocr_train and ocr_test
2. storename_features: find features from the text, and use xgboost to classify             
   input: ocr_train and ocr_test  
   output ocr_trainN, ocr_testN and scores                  
3. find_string: find Date, Subtotal and tax in the receipt                                 
   input: ocr testN, and scores           
   outout: full_submission
   
Need to rename the output files(delete the dates)
