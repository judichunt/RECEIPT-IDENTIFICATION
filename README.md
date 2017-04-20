# RECEIPT-IDENTIFICATION
Is this receipt a “Walmart” receipt – Yes/No?

1. pytesseract_test: extract words from photos     
   output: ocr_train and ocr_test＜/br＞
2. storename_features: find features from the text, and use xgboost to classify             
   input: ocr_train and ocr_test＜/br＞
   output ocr_trainN, ocr_testN and scores＜/br＞
3. find_string: find Date, Subtotal and tax in the receipt＜/br＞
   input: ocr testN, and scores＜/br＞
   outout: full_submission＜/br＞
