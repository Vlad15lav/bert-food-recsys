CONFIG = {
    "TOKEN": "YOUR TOKEN",
    "DATABASE": {
        "host": "YOUR HOST",
        "user": "YOUR USER",
        "passwd": "YOUR PASSWD",
        "database": "YOUR DATABASE NAME"
    },
    
    "A/B_STATUS": False,
    "MODEL_SELECT": "TF-IDF", # Options: "TF-IDF", "BERT"
    "DATA_ITEMS": "data/food-dataset-ru.csv",
    "BERT_ITEMS_PATH": "data/bert_items_embed.npy",
    "TFIDF_ITEMS_PATH": "data/tfidf_items_embed.npz",
    "TFIDF_FEATURES": "weights/tfidf-model.pkl",
    "TOKENIZER_PATH": "cointegrated/rubert-tiny2",
    "BERT_WEIGHT": "weights/bert-food-cls.pth",
    "BERT_CONFIG": {
        "architectures": [
        "BertForPreTraining"
        ],
        "attention_probs_dropout_prob": 0.1,
        "emb_size": 312,
        "gradient_checkpointing": False,
        "hidden_act": "gelu",
        "hidden_dropout_prob": 0.1,
        "hidden_size": 312,
        "initializer_range": 0.02,
        "intermediate_size": 600,
        "layer_norm_eps": 1e-12,
        "max_position_embeddings": 2048,
        "model_type": "bert",
        "num_attention_heads": 12,
        "num_hidden_layers": 3,
        "pad_token_id": 0,
        "position_embedding_type": "absolute",
        "torch_dtype": "float32",
        "transformers_version": "4.30.2",
        "type_vocab_size": 2,
        "use_cache": True,
        "vocab_size": 83828
    },
    "TOKENIZER": {
        "add_special_tokens": True,
        "max_length": 256,
        "padding": 'max_length',
        "truncation": True,
        "return_tensors": 'pt'
    }
}
