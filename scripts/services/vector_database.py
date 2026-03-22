import chromadb
from uuid import uuid4
from scripts.services.embedding_function import EmbeddingFunctionService


class VectorDatabase:
    """
        Classe com lógica específica para a indexação 
        de notícias em interação com banco de vetores.
    """
    def __init__(self) -> None:
        self.__client = chromadb.HttpClient()
        self.__collection = self.__client.get_or_create_collection(
            'noticias', embedding_function=EmbeddingFunctionService()
        )


    def inserir_noticia(self, conteudo: str):
        """Registra notícia no banco de vetores."""
        self.__collection.upsert(
            ids=[str(uuid4())], documents=[conteudo]
        )
    

    def get_maior_similaridade(self, conteudo: str) -> bool:
        """
            Busca o documento mais similar para verificar 
            se a mesma notícia já foi adicionada.
        """

        mais_similar = self.__collection.query(
            query_texts=[conteudo],
            n_results=1
        )
        similaridade = 1 - mais_similar.get('distances')[0]     # type: ignore

        return similaridade


    def deletar_noticias(self, id: int) -> None:
        """Deleta todos os registros do banco de vetores."""
        noticias = self.__collection.get()
        self.__collection.delete(
            ids=noticias.get('ids')
        )
    