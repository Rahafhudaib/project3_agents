from sentence_transformers import SentenceTransformer
import config

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def embed_texts(texts):
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def embed_query(text):
    model = get_model()
    return model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
