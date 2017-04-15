# RECEIPT-IDENTIFICATION
Is this receipt a “Walmart” receipt – Yes/No?

1. pytesseract_test: extract words from photos
2. storename_features: find features from the text, and use xgboost to classify
3. find_string: find Date, Subtotal and tax in the receipt
