from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import register_embedding_function
from chromadb import EmbeddingFunction, Embeddings, Documents
import os, dotenv

dotenv.load_dotenv()


@register_embedding_function
class EmbeddingFunctionService(EmbeddingFunction):
    def __init__(self, model: str = os.getenv('NOTIFICA_EMBEDDING_MODEL', '')) -> None:
        if not model:
            raise Exception('Modelo de embedding não detectado.')
        self.model = SentenceTransformer(model)

    
    def __call__(self, input: Documents) -> Embeddings:
        return self.model.encode(input).tolist()