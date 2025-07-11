```
backend/
├── .env
├── __init__.py  # initializes package
├── app.py  # main FastAPI app
├── generated_embedding
│   ├── embeddings_20250709_213158.npy
│   └── embeddings_20250709_213202.npy
├── images_taken
│   ├── ocr_2_20250711_155249.txt
│   ├── ocr_2_20250711_155255.txt
│   ├── ocr_2_20250711_155309.txt
│   ├── ocr_2_20250711_155317.txt
│   ├── ocr_2_20250711_155322.txt
│   ├── ocr_2_20250711_155330.txt
│   ├── ocr_3_20250711_155240.txt
│   ├── ocr_3_20250711_155304.txt
│   ├── ocr_3_20250711_155310.txt
│   └── ocr_3_20250711_155323.txt
├── img_vector_store
│   ├── index.faiss
│   └── index.pkl
├── recall_ai
│   ├── __init__.py  # initializes package
│   ├── config
│   │   ├── __init__.py  # initializes package
│   │   ├── gen_embeddings.py
│   │   ├── gen_vector_embedding.py
│   ├── embeddings
│   │   ├── __init__.py  # initializes package
│   │   ├── embedding.py
│   │   └── store_vector_embedding.py
│   ├── helpers
│   │   ├── __init__.py  # initializes package
│   │   ├── recall.py
│   │   └── utils.py  # utility functions
│   └── src
│       ├── __init__.py  # initializes package
│       └── mss_screen.py
└── requirements.txt
```